from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QComboBox, QLabel
from PySide6.QtCore import Signal
from utils.styles import StyleManager

class ToolbarWidget(QWidget):
    """工具栏组件"""
    
    # 信号定义
    search_changed = Signal(str)
    category_changed = Signal(str)
    add_clicked = Signal()
    refresh_clicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.apply_styles()
    
    def setup_ui(self):
        """设置UI"""
        layout = QHBoxLayout(self)
        layout.setSpacing(15)

        # 添加密码按钮
        self.add_btn = QPushButton('➕ 添加')
        self.add_btn.clicked.connect(self.add_clicked.emit)
        layout.addWidget(self.add_btn)
        
        # 搜索框
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText('🔍 搜索网站、用户名或备注...')
        self.search_edit.textChanged.connect(self.search_changed.emit)
        layout.addWidget(self.search_edit)
        
        self.category_combo = QComboBox()
        self.category_combo.currentTextChanged.connect(self._on_category_changed)
        layout.addWidget(self.category_combo)

        # 清除筛选按钮
        self.clear_filter_btn = QPushButton('🗑️ 重置')
        self.clear_filter_btn.clicked.connect(self.clear_all_filters)
        layout.addWidget(self.clear_filter_btn)
        
        # 刷新按钮
        self.refresh_btn = QPushButton('🔄 刷新')
        self.refresh_btn.clicked.connect(self.refresh_clicked.emit)
        layout.addWidget(self.refresh_btn)
    
    def _on_category_changed(self, text):
        """分类改变时的处理"""
        if text == '全部分类':
            self.category_changed.emit('')
        else:
            self.category_changed.emit(text)
    
    def apply_styles(self):
        """应用样式"""
        self.search_edit.setStyleSheet(StyleManager.get_input_style())
        self.category_combo.setStyleSheet(StyleManager.get_combobox_style())
        self.add_btn.setStyleSheet(StyleManager.get_button_style())
        self.clear_filter_btn.setStyleSheet(StyleManager.get_secondary_button_style())
        self.refresh_btn.setStyleSheet(StyleManager.get_secondary_button_style())
    
    def get_search_text(self):
        """获取搜索文本"""
        return self.search_edit.text()
    
    def get_selected_category(self):
        """获取选中的分类"""
        current_data = self.category_combo.currentData()
        if current_data is not None:
            return current_data
        return self.category_combo.currentText() if self.category_combo.currentText() != '全部分类' else ''
    
    def clear_search(self):
        """清空搜索框"""
        self.search_edit.clear()
    
    def reset_category(self):
        """重置分类筛选"""
        self.category_combo.setCurrentIndex(0)
    
    def update_categories(self, categories):
        """更新分类列表"""
        current_selection = self.get_selected_category()
        
        # 清空并重新添加
        self.category_combo.clear()
        self.category_combo.addItem('全部分类', '')
        
        # 添加预设分类
        default_categories = [
            '工作', '本地', '个人', '全链路'
        ]
        
        # 合并用户自定义分类
        all_categories = list(set(default_categories + [cat for cat in categories if cat and cat not in default_categories]))
        all_categories.sort()
        
        for category in all_categories:
            self.category_combo.addItem(category)
        
        # 添加未分类选项
        self.category_combo.addItem('未分类')
        
        # 恢复之前的选择
        if current_selection:
            index = self.category_combo.findText(current_selection)
            if index >= 0:
                self.category_combo.setCurrentIndex(index)

    def clear_all_filters(self):
        """清除所有筛选条件"""
        self.clear_search()
        self.reset_category()
