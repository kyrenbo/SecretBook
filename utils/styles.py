class StyleManager:
    """样式管理器"""
    
    @staticmethod
    def get_input_style():
        """获取输入框样式"""
        return """
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 5px 10px;
                font-size: 13px;
                font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
                background-color: #ffffff;
                margin: 10px 0px;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
                background-color: #f9f9f9;
            }
            QLineEdit:hover {
                border-color: #c0c0c0;
            }
        """
    
    @staticmethod
    def get_combobox_style():
        """获取下拉框样式"""
        return """
            QComboBox {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 5px 10px;
                font-size: 13px;
                font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
                background-color: #ffffff;
                margin: 10px 0px;
                min-width: 120px;
                padding-right: 25px;
            }
            QComboBox:focus {
                border-color: #4CAF50;
                background-color: #f9f9f9;
            }
            QComboBox:hover {
                border-color: #c0c0c0;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #e0e0e0;
                border-left-style: solid;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
                background-color: #f8f8f8;
            }
            QComboBox::drop-down:hover {
                background-color: #e8e8e8;
            }
            QComboBox::down-arrow {
                image: none;
                font-family: 'Arial';
                font-size: 12px;
                color: #666666;
                width: 12px;
                height: 12px;
            }
            QComboBox::down-arrow:after {
                content: '▼';
            }
            QComboBox::down-arrow:hover {
                border-top-color: #333333;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background-color: #ffffff;
                selection-background-color: #4CAF50;
                selection-color: white;
                font-size: 13px;
                font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
                padding: 5px;
                outline: none;
            }
            QComboBox QAbstractItemView::item {
                padding: 8px 10px;
                border-radius: 4px;
                margin: 1px;
                min-height: 20px;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #f0f8f0;
                color: #2c3e50;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #4CAF50;
                color: white;
            }
        """
    
    @staticmethod
    def get_textarea_style():
        """获取文本域样式"""
        return """
            QTextEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 5px 10px;
                font-size: 13px;
                font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
                background-color: #ffffff;
                margin: 5px 0px;
                min-height: 50px;
            }
            QTextEdit:focus {
                border-color: #4CAF50;
                background-color: #f9f9f9;
            }
            QTextEdit:hover {
                border-color: #c0c0c0;
            }
        """
    
    @staticmethod
    def get_button_style():
        """获取按钮样式"""
        return """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
                font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
                font-weight: 500;
                margin: 5px 2px;
            }
            QPushButton:hover {
                background-color: #45a049;
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """
    
    @staticmethod
    def get_secondary_button_style():
        """获取次要按钮样式"""
        return """
            QPushButton {
                background-color: #f0f0f0;
                color: #333333;
                border: none;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
                font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
                font-weight: 500;
                margin: 5px 2px;
            }
            QPushButton:hover {
                background-color: #e8e8e8;
                border-color: #c0c0c0;
            }
            QPushButton:pressed {
                background-color: #d8d8d8;
            }
        """
    
    @staticmethod
    def get_danger_button_style():
        """获取危险按钮样式"""
        return """
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
                font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
                font-weight: 500;
                margin: 5px 2px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #c62828;
            }
        """
    
    @staticmethod
    def get_dialog_style():
        """获取对话框样式"""
        return """
            QDialog {
                background-color: #ffffff;
                font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
                color: #333333;
                margin: 5px 0px;
            }
        """
    
    @staticmethod
    def get_main_window_style():
        """获取主窗口样式"""
        return """
            QMainWindow {
                background-color: #f5f5f5;
                font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
            }
            QWidget {
                font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
            }
        """

    @staticmethod
    def get_msg_box_style():
        """获取消息提示样式"""
        return """
            QMessageBox {
                background-color: #ffffff;
                font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
                border-radius: 8px;
            }
            QMessageBox QLabel { 
                color: #333333;
                font-size: 13px;
                font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
            }
            QMessageBox QPushButton {
                background-color: #4CAF50;
                color: white;
                min-width: 80px;
                min-height: 30px;
                border: none;
                border-radius: 5px;
                font-size: 13px;
                font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
                margin: 5px;
            }
            QMessageBox QPushButton:hover {
                background-color: #45a049;
            }
            QMessageBox QPushButton:pressed {
                background-color: #3d8b40;
            }
        """