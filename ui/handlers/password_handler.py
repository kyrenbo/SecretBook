from PySide6.QtWidgets import QMessageBox, QDialog
from PySide6.QtCore import QObject, Signal
from ..password_dialog import PasswordDialog
from ..login_dialog import LoginDialog

class PasswordHandler(QObject):
    """密码业务逻辑处理器"""
    
    # 信号定义
    passwords_updated = Signal()
    status_message = Signal(str, int)  # message, timeout
    
    def __init__(self, data_manager, parent_window):
        super().__init__()
        self.data_manager = data_manager
        self.parent_window = parent_window
    
    def add_password(self):
        """添加密码"""
        dialog = PasswordDialog()
        if dialog.exec() == QDialog.Accepted:
            password_data = dialog.get_data()
            
            # 检查唯一性
            success, message, duplicate_data = self.data_manager.save_password(password_data)
            
            if not success and duplicate_data:
                # 发现重复，询问用户
                reply = QMessageBox.question(
                    self.parent_window,
                    '发现重复密码',
                    f'应用名：{password_data.get("website", "")}\n'
                    f'用户名：{password_data.get("username", "")}\n\n'
                    f'该密码已存在，是否要更新现有密码？\n\n'
                    f'现有密码创建时间：{duplicate_data.get("created_at", "未知")}',
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                
                if reply == QMessageBox.Yes:
                    # 用户选择更新
                    success, message, _ = self.data_manager.update_password(
                        duplicate_data['id'], password_data, force_update=True
                    )
                    
                    if success:
                        QMessageBox.information(self.parent_window, '成功', '密码已更新')
                        self.passwords_updated.emit()
                    else:
                        QMessageBox.critical(self.parent_window, '错误', f'更新失败：{message}')
            elif success:
                QMessageBox.information(self.parent_window, '成功', '密码已添加')
                self.passwords_updated.emit()
            else:
                QMessageBox.critical(self.parent_window, '错误', f'添加失败：{message}')
    
    def edit_password(self, password):
        """编辑密码"""
        dialog = PasswordDialog(password)
        if dialog.exec() == QDialog.Accepted:
            password_data = dialog.get_data()
            
            # 检查唯一性
            success, message, duplicate_data = self.data_manager.update_password(
                password['id'], password_data
            )
            
            if not success and duplicate_data:
                # 发现重复，询问用户
                reply = QMessageBox.question(
                    self.parent_window,
                    '发现重复密码',
                    f'应用名：{password_data.get("website", "")}\n'
                    f'用户名：{password_data.get("username", "")}\n\n'
                    f'该密码已存在，是否要强制更新？\n\n'
                    f'冲突密码创建时间：{duplicate_data.get("created_at", "未知")}',
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                
                if reply == QMessageBox.Yes:
                    # 用户选择强制更新
                    success, message, _ = self.data_manager.update_password(
                        password['id'], password_data, force_update=True
                    )
                    
                    if success:
                        QMessageBox.information(self.parent_window, '成功', '密码已更新')
                        self.passwords_updated.emit()
                    else:
                        QMessageBox.critical(self.parent_window, '错误', f'更新失败：{message}')
            elif success:
                QMessageBox.information(self.parent_window, '成功', '密码已更新')
                self.passwords_updated.emit()
            else:
                QMessageBox.critical(self.parent_window, '错误', f'更新失败：{message}')
    
    def delete_password(self, password):
        """删除密码"""
        reply = QMessageBox.question(
            self.parent_window, '确认删除',
            f'确定要删除 "{password.get("website", "")}" 的密码吗？',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.data_manager.delete_password(password['id']):
                self.passwords_updated.emit()
                self.status_message.emit('密码删除成功', 2000)
            else:
                QMessageBox.warning(self.parent_window, '错误', '密码删除失败')
    
    def logout(self):
        """注销"""
        reply = QMessageBox.question(
            self.parent_window, '确认注销',
            '确定要注销当前用户吗？',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.parent_window.close()
            # 重新显示登录对话框
            login_dialog = LoginDialog(self.data_manager)
            if login_dialog.exec() == QDialog.Accepted:
                # 创建新的主窗口
                from ..main_window import MainWindow
                new_window = MainWindow(self.data_manager)
                new_window.show()