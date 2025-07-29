import os

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QMessageBox, QApplication
)

from utils.icon_manager import IconManager
from utils.styles import StyleManager
from utils.data_manager import DataManager
from .components.toolbar import ToolbarWidget
from .components.password_table import PasswordTableWidget
from .components.menu_manager import MenuManager
from .handlers.password_handler import PasswordHandler
from .handlers.import_export_handler import ImportExportHandler

class MainWindow(QMainWindow):
    """主窗口 - 重构后的简洁版本"""
    
    def __init__(self, data_manager: DataManager):
        super().__init__()
        self.data_manager = data_manager
        self.passwords = []

        # 初始化组件
        self.init_components()
        self.setup_ui()
        self.connect_signals()
        self.apply_styles()
        self.load_passwords()
    
    def init_components(self):
        """初始化组件"""
        # 创建处理器
        self.password_handler = PasswordHandler(self.data_manager, self)
        self.import_export_handler = ImportExportHandler(self.data_manager, self)
        
        # 创建UI组件
        self.toolbar = ToolbarWidget()
        self.password_table = PasswordTableWidget()
        self.menu_manager = MenuManager(self)
    
    def setup_ui(self):
        """设置UI布局"""
        self.setWindowTitle(f' 密码本 - {self.data_manager.current_user}')

        # 设置窗口图标
        IconManager.set_window_icon(self)

        self.resize(900, 650)
        self.center_window()
        
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(0)
        layout.setContentsMargins(20, 0, 20, 20)
        
        # 添加组件
        layout.addWidget(self.toolbar)
        layout.addWidget(self.password_table)
        
        # 状态栏
        self.setup_status_bar()

    def set_window_icon(self):
        """设置窗口图标"""
        try:
            # 获取logo文件路径
            current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            logo_path = os.path.join(current_dir, 'assets', 'logo.svg')

            if os.path.exists(logo_path):
                icon = QIcon(logo_path)
                self.setWindowIcon(icon)
            else:
                # 如果logo文件不存在，使用emoji作为标题
                self.setWindowTitle(f'🔐 密码本 - {self.data_manager.current_user}')
        except Exception as e:
            print(f"设置图标失败: {e}")
            # 使用emoji作为备选方案
            self.setWindowTitle(f'🔐 密码本 - {self.data_manager.current_user}')
    
    def setup_status_bar(self):
        """设置状态栏"""
        self.statusBar().showMessage('就绪')
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background-color: #f8f9fa;
                color: #6c757d;
                border-top: 1px solid #e0e0e0;
                font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
                padding: 8px;
            }
        """)
    
    def connect_signals(self):
        """连接信号"""
        # 工具栏信号
        self.toolbar.search_changed.connect(self.filter_passwords)
        self.toolbar.category_changed.connect(self.filter_passwords_by_category)
        self.toolbar.add_clicked.connect(self.password_handler.add_password)
        self.toolbar.refresh_clicked.connect(self.load_passwords)
        
        # 表格信号
        self.password_table.password_copied.connect(self.show_status_message)
        self.password_table.password_edit_requested.connect(self.password_handler.edit_password)
        self.password_table.password_delete_requested.connect(self.password_handler.delete_password)
        
        # 菜单信号
        self.menu_manager.add_password_requested.connect(self.password_handler.add_password)
        self.menu_manager.export_requested.connect(self.import_export_handler.export_passwords)
        self.menu_manager.import_requested.connect(self.import_export_handler.import_passwords)
        self.menu_manager.logout_requested.connect(self.password_handler.logout)
        self.menu_manager.about_requested.connect(self.show_about)
        
        # 处理器信号
        self.password_handler.passwords_updated.connect(self.load_passwords)
        self.password_handler.status_message.connect(self.show_status_message)
    
    def apply_styles(self):
        """应用样式"""
        self.setStyleSheet(StyleManager.get_main_window_style())
    
    def load_passwords(self):
        """加载密码列表"""
        self.passwords = self.data_manager.get_user_passwords()
        self.password_table.update_data(self.passwords)
        self.statusBar().showMessage(f'共 {len(self.passwords)} 条密码记录')
        
        # 更新分类列表
        categories = list(set([pwd.get('category', '') for pwd in self.passwords if pwd.get('category')]))
        self.toolbar.update_categories(categories)

    def filter_passwords(self, search_text=None):
        """过滤密码"""
        if search_text is None:
            search_text = self.toolbar.get_search_text()
        
        selected_category = self.toolbar.get_selected_category()
        
        filtered_passwords = self.passwords
        
        # 按分类筛选
        if selected_category:
            if selected_category == '未分类':
                filtered_passwords = [pwd for pwd in filtered_passwords if not pwd.get('category')]
            else:
                filtered_passwords = [pwd for pwd in filtered_passwords if pwd.get('category') == selected_category]
        
        # 按搜索文本筛选
        if search_text:
            search_text = search_text.lower()
            filtered_passwords = [
                pwd for pwd in filtered_passwords
                if (search_text in pwd.get('website', '').lower() or
                    search_text in pwd.get('username', '').lower() or
                    search_text in pwd.get('notes', '').lower() or
                    search_text in pwd.get('category', '').lower())
            ]
        
        self.password_table.update_data(filtered_passwords)
        self.statusBar().showMessage(f'显示 {len(filtered_passwords)} 条记录')

    def filter_passwords_by_category(self, category):
        """按分类筛选密码"""
        self.filter_passwords()
    
    def show_status_message(self, message, timeout=2000):
        """显示状态消息"""
        self.statusBar().showMessage(message, timeout)
    
    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(
            self, '关于密码本',
            '密码本 v1.0\n\n'
            '一个简单安全的密码管理工具\n\n'
            '功能特点：\n'
            '• 本地加密存储\n'
            '• 用户账户管理\n'
            '• 密码安全查看\n'
            '• 一键复制功能\n'
            '• 搜索过滤功能\n\n'
            '开发：Python + PySide6'
        )
    
    def center_window(self):
        """将窗口居中显示"""
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )