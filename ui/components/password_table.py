from PySide6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QHeaderView, QWidget, 
    QHBoxLayout, QPushButton, QAbstractItemView, QApplication
)
from PySide6.QtCore import Qt, Signal

class PasswordTableWidget(QTableWidget):
    """密码表格组件"""
    
    # 信号定义
    password_copied = Signal(str)
    password_edit_requested = Signal(dict)
    password_delete_requested = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.apply_styles()
    
    def setup_ui(self):
        """设置UI"""
        self.setColumnCount(8)  # 增加一列
        self.setHorizontalHeaderLabels([
            '序号', '网站/应用', '分类', '用户名', '密码', '网址', '备注', '操作'
        ])
        
        # 设置表格不可编辑
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        # 设置行高
        self.verticalHeader().setDefaultSectionSize(42)
        self.verticalHeader().setVisible(False)
        
        # 设置列宽
        self.setup_column_widths()
    
    def setup_column_widths(self):
        """设置列宽"""
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)  # 序号列固定宽度
        header.resizeSection(0, 60)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # 网站/应用
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # 分类
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # 用户名
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # 密码
        header.setSectionResizeMode(5, QHeaderView.Stretch)  # 网址
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # 备注
        header.setSectionResizeMode(7, QHeaderView.Fixed)  # 操作列固定宽度
        header.resizeSection(7, 150)
    
    def apply_styles(self):
        """应用样式"""
        self.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background-color: white;
                gridline-color: #f0f0f0;
                font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
                font-size: 13px;
                selection-background-color: transparent;
            }
            QTableWidget::item {
                padding: 4px 12px;
                border-bottom: 1px solid #f0f0f0;
                min-height: 40px;
                selection-background-color: transparent;
            }
            QTableWidget::item:selected {
                background-color: transparent;
                color: inherit;
            }
            QTableWidget::item:focus {
                background-color: transparent;
                outline: none;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 12px 10px;
                border: none;
                border-bottom: 2px solid #e0e0e0;
                font-weight: 600;
                color: #2c3e50;
                min-height: 35px;
            }
        """)
    
    def update_data(self, passwords):
        """更新表格数据"""
        self.setRowCount(len(passwords))
        
        for row, password in enumerate(passwords):
            self.populate_row(row, password)
    
    def populate_row(self, row, password):
        """填充行数据"""
        # 序号
        sequence_item = QTableWidgetItem(str(row + 1))
        sequence_item.setTextAlignment(Qt.AlignCenter)
        self.setItem(row, 0, sequence_item)
        
        # 网站/应用
        self.setItem(row, 1, QTableWidgetItem(password.get('website', '')))
        
        # 分类
        category_item = QTableWidgetItem(password.get('category', '未分类'))
        category_item.setTextAlignment(Qt.AlignCenter)
        self.setItem(row, 2, category_item)
        
        # 用户名
        self.setItem(row, 3, QTableWidgetItem(password.get('username', '')))
        
        # 密码（隐藏显示）
        password_item = QTableWidgetItem('••••••••')
        password_item.setData(Qt.UserRole, password.get('password', ''))
        self.setItem(row, 4, password_item)
        
        # 网址
        self.setItem(row, 5, QTableWidgetItem(password.get('url', '')))
        
        # 备注
        notes = password.get('notes', '')
        if len(notes) > 20:
            notes = notes[:20] + '...'
        self.setItem(row, 6, QTableWidgetItem(notes))
        
        # 操作按钮
        self.create_action_buttons(row, password)
    
    def create_action_buttons(self, row, password):
        """创建操作按钮"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setSpacing(2)
        
        # 按钮样式
        small_button_style = """
            QPushButton {
                border: none;
                border-radius: 4px;
                font-size: 11px;
                font-weight: 500;
                margin: 1px;
                min-width: 28px;
                min-height: 28px;
            }
        """
        
        # 复制密码按钮
        copy_btn = QPushButton('📋')
        copy_btn.setToolTip('复制密码')
        copy_btn.setFixedSize(32, 28)
        copy_btn.setStyleSheet(small_button_style + """
            QPushButton {
                background-color: #17a2b8;
                color: white;
            }
            QPushButton:hover {
                background-color: #138496;
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background-color: #117a8b;
            }
        """)
        copy_btn.clicked.connect(lambda: self.copy_password(password.get('password', '')))
        layout.addWidget(copy_btn)
        
        # 查看按钮
        view_btn = QPushButton('👁️')
        view_btn.setToolTip('查看密码')
        view_btn.setFixedSize(32, 28)
        view_btn.setStyleSheet(small_button_style + """
            QPushButton {
                background-color: #6c757d;
                color: white;
            }
            QPushButton:hover {
                background-color: #5a6268;
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background-color: #545b62;
            }
        """)
        view_btn.clicked.connect(lambda: self.toggle_password_visibility(row))
        layout.addWidget(view_btn)
        
        # 编辑按钮
        edit_btn = QPushButton('✏️')
        edit_btn.setToolTip('编辑')
        edit_btn.setFixedSize(32, 28)
        edit_btn.setStyleSheet(small_button_style + """
            QPushButton {
                background-color: #28a745;
                color: white;
            }
            QPushButton:hover {
                background-color: #218838;
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        edit_btn.clicked.connect(lambda: self.password_edit_requested.emit(password))
        layout.addWidget(edit_btn)
        
        # 删除按钮
        delete_btn = QPushButton('🗑️')
        delete_btn.setToolTip('删除')
        delete_btn.setFixedSize(32, 28)
        delete_btn.setStyleSheet(small_button_style + """
            QPushButton {
                background-color: #dc3545;
                color: white;
            }
            QPushButton:hover {
                background-color: #c82333;
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
        """)
        delete_btn.clicked.connect(lambda: self.password_delete_requested.emit(password))
        layout.addWidget(delete_btn)
        
        self.setCellWidget(row, 7, widget)
    
    def copy_password(self, password):
        """复制密码到剪贴板"""
        clipboard = QApplication.clipboard()
        clipboard.setText(password)
        self.password_copied.emit('密码已复制到剪贴板')
    
    def toggle_password_visibility(self, row):
        """切换密码可见性"""
        item = self.item(row, 4)  # 密码列索引改为4
        if item:
            current_text = item.text()
            real_password = item.data(Qt.UserRole)
            
            if current_text == '••••••••':
                item.setText(real_password)
            else:
                item.setText('••••••••')