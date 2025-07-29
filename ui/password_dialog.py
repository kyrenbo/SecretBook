from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QFormLayout, QTextEdit, QComboBox, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from utils.icon_manager import IconManager
from utils.styles import StyleManager


class PasswordDialog(QDialog):
    """密码编辑对话框"""
    
    def __init__(self, password_data=None):
        super().__init__()
        self.password_data = password_data
        self.setup_ui()
        self.apply_styles()
        
        if password_data:
            self.load_data()
    
    def setup_ui(self):
        # 设置窗口图标
        IconManager.set_window_icon(self)
        self.setWindowTitle('添加密码' if not self.password_data else '编辑密码')
        self.setFixedSize(430, 550)  # 增加高度以容纳分类字段
        self.setModal(True)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 标题
        title = QLabel('添加新密码' if not self.password_data else '编辑密码')
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Microsoft YaHei', 16, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # 表单
        form_layout = QFormLayout()
        form_layout.setSpacing(5)
        
        # 网站/应用 (必填)
        website_label = QLabel('<span style="color: red;">*</span>网站/应用: ')
        website_label.setFont(QFont('Microsoft YaHei', 12))
        website_label.setStyleSheet("color: #34495e; font-weight: 500;")
        
        self.website_edit = QLineEdit()
        self.website_edit.setPlaceholderText('如：百度、QQ、微信等（必填）')
        form_layout.addRow(website_label, self.website_edit)
        
        # 分类
        category_label = QLabel('分类:')
        category_label.setFont(QFont('Microsoft YaHei', 12))
        category_label.setStyleSheet("color: #34495e; font-weight: 500;")
        
        self.category_combo = QComboBox()
        self.category_combo.setEditable(True)  # 允许用户输入自定义分类
        self.category_combo.addItems([
            '未分类', '工作', '本地', '个人', '全链路'
        ])
        self.category_combo.setCurrentText('未分类')  # 默认为空
        form_layout.addRow(category_label, self.category_combo)
        
        # 用户名 (必填)
        username_label = QLabel('<span style="color: red;">*</span>账号: ')
        username_label.setFont(QFont('Microsoft YaHei', 12))
        username_label.setStyleSheet("color: #34495e; font-weight: 500;")
        
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText('用户名、电话或邮箱（必填）')
        form_layout.addRow(username_label, self.username_edit)
        
        # 密码 (必填)
        password_label = QLabel('<span style="color: red;">*</span>密码: ')
        password_label.setFont(QFont('Microsoft YaHei', 12))
        password_label.setStyleSheet("color: #34495e; font-weight: 500;")
        
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setPlaceholderText('密码（必填）')
        form_layout.addRow(password_label, self.password_edit)
        
        # 网址
        url_label = QLabel('网址:')
        url_label.setFont(QFont('Microsoft YaHei', 12))
        url_label.setStyleSheet("color: #34495e; font-weight: 500;")
        
        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText('网站地址（可选）')
        form_layout.addRow(url_label, self.url_edit)
        
        # 备注
        notes_label = QLabel('备注:')
        notes_label.setFont(QFont('Microsoft YaHei', 12))
        notes_label.setStyleSheet("color: #34495e; font-weight: 500;")
        
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText('备注信息（可选）')
        self.notes_edit.setMaximumHeight(120)
        self.notes_edit.setMinimumHeight(80)
        form_layout.addRow(notes_label, self.notes_edit)
        
        layout.addLayout(form_layout)
        
        # 按钮
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.save_btn = QPushButton('保存')
        self.save_btn.clicked.connect(self.validate_and_save)
        
        self.cancel_btn = QPushButton('取消')
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def validate_and_save(self):
        """验证必填项并保存"""
        # 获取必填字段的值
        website = self.website_edit.text().strip()
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()
        
        # 验证必填项
        if not website:
            self.show_validation_error('请输入网站/应用名称')
            self.website_edit.setFocus()
            return
        
        if not username:
            self.show_validation_error('请输入用户名')
            self.username_edit.setFocus()
            return
        
        if not password:
            self.show_validation_error('请输入密码')
            self.password_edit.setFocus()
            return
        
        # 验证通过，接受对话框
        self.accept()
    
    def show_validation_error(self, message):
        """显示验证错误消息"""
        msg_box = QMessageBox(self)
        msg_box.setStyleSheet(StyleManager.get_msg_box_style())
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle('输入验证')
        msg_box.setText(message)
        msg_box.exec()
    
    def apply_styles(self):
        """应用样式"""
        self.setStyleSheet(StyleManager.get_dialog_style())
        self.website_edit.setStyleSheet(StyleManager.get_input_style())
        self.category_combo.setStyleSheet(StyleManager.get_combobox_style())
        self.username_edit.setStyleSheet(StyleManager.get_input_style())
        self.password_edit.setStyleSheet(StyleManager.get_input_style())
        self.url_edit.setStyleSheet(StyleManager.get_input_style())
        self.notes_edit.setStyleSheet(StyleManager.get_textarea_style())
        self.save_btn.setStyleSheet(StyleManager.get_button_style())
        self.cancel_btn.setStyleSheet(StyleManager.get_secondary_button_style())
    
    def load_data(self):
        """加载密码数据"""
        self.website_edit.setText(self.password_data.get('website', ''))
        self.category_combo.setCurrentText(self.password_data.get('category', ''))
        self.username_edit.setText(self.password_data.get('username', ''))
        self.password_edit.setText(self.password_data.get('password', ''))
        self.url_edit.setText(self.password_data.get('url', ''))
        self.notes_edit.setPlainText(self.password_data.get('notes', ''))
    
    def get_data(self) -> dict:
        """获取表单数据"""
        return {
            'website': self.website_edit.text().strip(),
            'category': self.category_combo.currentText().strip(),
            'username': self.username_edit.text().strip(),
            'password': self.password_edit.text(),
            'url': self.url_edit.text().strip(),
            'notes': self.notes_edit.toPlainText().strip()
        }