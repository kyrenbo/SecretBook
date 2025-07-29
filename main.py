import sys
from PySide6.QtWidgets import QApplication, QDialog

from ui.main_window import MainWindow
from ui.login_dialog import LoginDialog
from utils.data_manager import DataManager


class SecretBookApp:
    """密码本应用程序"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName('密码本')
        self.app.setApplicationVersion('1.0')
        
        self.data_manager = DataManager()
        
        # 设置应用图标（如果有的话）
        # self.app.setWindowIcon(QIcon('icon.png'))
    
    def run(self):
        """运行应用程序"""
        # 显示登录对话框
        login_dialog = LoginDialog(self.data_manager)
        
        if login_dialog.exec() == QDialog.Accepted:
            # 登录成功，显示主窗口
            main_window = MainWindow(self.data_manager)
            main_window.show()
            
            return self.app.exec()
        else:
            # 用户取消登录
            return 0

if __name__ == '__main__':
    try:
        app = SecretBookApp()
        sys.exit(app.run())
    except Exception as e:
        print(f"应用程序启动失败: {e}")
        sys.exit(1)
