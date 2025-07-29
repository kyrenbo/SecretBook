from PySide6.QtGui import QAction
from PySide6.QtCore import QObject, Signal

class MenuManager(QObject):
    """菜单管理器"""
    
    # 信号定义
    add_password_requested = Signal()
    export_requested = Signal()
    import_requested = Signal()
    logout_requested = Signal()
    about_requested = Signal()
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_menu()
    
    def setup_menu(self):
        """设置菜单"""
        menubar = self.main_window.menuBar()
        self.apply_menu_styles(menubar)
        
        # 文件菜单
        self.create_file_menu(menubar)
        
        # 帮助菜单
        self.create_help_menu(menubar)
    
    def apply_menu_styles(self, menubar):
        """应用菜单样式"""
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #ffffff;
                color: #2c3e50;
                border-bottom: 1px solid #e0e0e0;
                font-size: 13px;
                font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
                padding: 5px;
            }
            QMenuBar::item {
                padding: 8px 12px;
                margin: 2px;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background-color: #f0f0f0;
            }
            QMenu {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 5px;
            }
            QMenu::item {
                padding: 6px 15px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #f0f0f0;
            }
        """)
    
    def create_file_menu(self, menubar):
        """创建文件菜单"""
        file_menu = menubar.addMenu('文件')
        
        # 添加密码
        add_action = QAction('添加密码', self.main_window)
        add_action.setShortcut('Ctrl+N')
        add_action.triggered.connect(self.add_password_requested.emit)
        file_menu.addAction(add_action)
        
        file_menu.addSeparator()
        
        # 导出密码
        export_action = QAction('导出密码...', self.main_window)
        export_action.setShortcut('Ctrl+E')
        export_action.triggered.connect(self.export_requested.emit)
        file_menu.addAction(export_action)
        
        # 导入密码
        import_action = QAction('导入密码...', self.main_window)
        import_action.setShortcut('Ctrl+I')
        import_action.triggered.connect(self.import_requested.emit)
        file_menu.addAction(import_action)
        
        file_menu.addSeparator()
        
        # 注销
        logout_action = QAction('注销', self.main_window)
        logout_action.triggered.connect(self.logout_requested.emit)
        file_menu.addAction(logout_action)
        
        # 退出
        exit_action = QAction('退出', self.main_window)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.main_window.close)
        file_menu.addAction(exit_action)
    
    def create_help_menu(self, menubar):
        """创建帮助菜单"""
        help_menu = menubar.addMenu('帮助')
        
        about_action = QAction('关于', self.main_window)
        about_action.triggered.connect(self.about_requested.emit)
        help_menu.addAction(about_action)