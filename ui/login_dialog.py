from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QFormLayout, QMessageBox, QCheckBox
)
from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QFont, QIcon

from utils.icon_manager import IconManager
from utils.styles import StyleManager
from utils.data_manager import DataManager


class LoginDialog(QDialog):
    """登录对话框"""
    
    def __init__(self, data_manager: DataManager):
        super().__init__()
        self.data_manager = data_manager
        self.settings = QSettings('SecretBook', 'LoginSettings')
        self.setup_ui()
        self.apply_styles()
        self.load_saved_settings()
    
    def setup_ui(self):
        IconManager.set_window_icon(self)
        self.setWindowTitle('密码本 - 登录')
        self.setFixedSize(400, 350)  # 减少高度，因为移除了一个复选框
        self.setModal(True)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 标题
        title = QLabel('🔐 密码管理')
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Microsoft YaHei', 20, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)
        
        # 表单
        form_layout = QFormLayout()
        form_layout.setSpacing(7)
        
        # 用户名标签
        username_label = QLabel('用户名:')
        username_label.setFont(QFont('Microsoft YaHei', 12))
        username_label.setStyleSheet("color: #34495e; font-weight: 500;")
        
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText('请输入用户名')
        form_layout.addRow(username_label, self.username_edit)
        
        # 密码标签
        password_label = QLabel('密码:')
        password_label.setFont(QFont('Microsoft YaHei', 12))
        password_label.setStyleSheet("color: #34495e; font-weight: 500;")
        
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setPlaceholderText('请输入密码')
        form_layout.addRow(password_label, self.password_edit)
        
        layout.addLayout(form_layout)
        
        # 记住密码选项（移除记住用户名选项）
        remember_layout = QVBoxLayout()
        remember_layout.setSpacing(8)
        
        self.remember_password_cb = QCheckBox('记住密码')
        self.remember_password_cb.setFont(QFont('Microsoft YaHei', 10))
        self.remember_password_cb.setStyleSheet("""
            QCheckBox {
                color: #34495e;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #bdc3c7;
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #3498db;
                border-color: #3498db;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDQuNUw0LjUgOEwxMSAxIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
            }
        """)
        remember_layout.addWidget(self.remember_password_cb)
        
        layout.addLayout(remember_layout)
        
        # 按钮
        button_layout = QHBoxLayout()
        button_layout.setSpacing(30)
        
        self.login_btn = QPushButton('登录')
        self.login_btn.clicked.connect(self.login)
        
        self.register_btn = QPushButton('注册')
        self.register_btn.clicked.connect(self.register)
        
        button_layout.addWidget(self.login_btn)
        button_layout.addWidget(self.register_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # 回车登录
        self.password_edit.returnPressed.connect(self.login)
    
    def load_saved_settings(self):
        """加载保存的设置"""
        # 默认总是记住用户名，自动加载保存的用户名
        saved_username = self.settings.value('username', '')
        if saved_username:
            self.username_edit.setText(saved_username)
        
        # 加载记住密码设置
        remember_password = self.settings.value('remember_password', False, type=bool)
        self.remember_password_cb.setChecked(remember_password)
        
        if remember_password:
            saved_password = self.settings.value('password', '')
            self.password_edit.setText(saved_password)
    
    def save_settings(self):
        """保存设置"""
        # 默认总是保存用户名
        self.settings.setValue('username', self.username_edit.text())
        
        # 保存记住密码设置
        self.settings.setValue('remember_password', self.remember_password_cb.isChecked())
        if self.remember_password_cb.isChecked():
            self.settings.setValue('password', self.password_edit.text())
        else:
            self.settings.remove('password')
    
    def apply_styles(self):
        """应用样式"""
        self.setStyleSheet(StyleManager.get_dialog_style())
        self.username_edit.setStyleSheet(StyleManager.get_input_style())
        self.password_edit.setStyleSheet(StyleManager.get_input_style())
        self.login_btn.setStyleSheet(StyleManager.get_button_style())
        self.register_btn.setStyleSheet(StyleManager.get_secondary_button_style())
    
    def show_message(self, icon_type, title, message):
        """显示消息框的通用方法
        
        Args:
            icon_type: 消息框图标类型 (QMessageBox.Warning, QMessageBox.Information, etc.)
            title: 消息框标题
            message: 消息内容
        """
        qmb = QMessageBox(self)
        qmb.setStyleSheet(StyleManager.get_msg_box_style())
        qmb.setIcon(icon_type)
        qmb.setWindowTitle(title)
        qmb.setText(message)
        qmb.exec()
    
    def login(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        
        if not username or not password:
            self.show_message(QMessageBox.Warning, '警告', '请输入用户名和密码')
            return
        
        if self.data_manager.login_user(username, password):
            self.save_settings()  # 登录成功后保存设置
            self.accept()
        else:
            self.show_message(QMessageBox.Warning, '登录失败', '用户名或密码错误')
            self.password_edit.clear()
    
    def register(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        
        if not username or not password:
            self.show_message(QMessageBox.Warning, '警告', '请输入用户名和密码')
            return
        
        if len(password) < 6:
            self.show_message(QMessageBox.Warning, '警告', '密码长度至少6位')
            return
        
        if self.data_manager.register_user(username, password):
            self.show_message(QMessageBox.Information, '注册成功', '用户注册成功，请登录')
            self.password_edit.clear()
        else:
            self.show_message(QMessageBox.Warning, '注册失败', '用户名已存在')