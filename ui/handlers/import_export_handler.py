from PySide6.QtWidgets import QMessageBox, QFileDialog
from PySide6.QtCore import QObject, Signal
from datetime import datetime

class ImportExportHandler(QObject):
    """导入导出处理器"""
    
    # 信号定义
    passwords_updated = Signal()
    
    def __init__(self, data_manager, parent_window):
        super().__init__()
        self.data_manager = data_manager
        self.parent_window = parent_window

    def export_passwords(self):
        """导出密码"""
        # 从主窗口获取密码数据
        passwords = self.parent_window.passwords
        
        if not passwords:
            QMessageBox.information(self.parent_window, '提示', '没有密码数据可以导出')
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self.parent_window,
            '导出密码',
            f'密码导出_{self.data_manager.current_user}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.sbk',
            'SecretBook文件 (*.sbk);;所有文件 (*)'
        )

        if file_path:
            if self.data_manager.export_passwords(file_path):
                QMessageBox.information(
                    self.parent_window,
                    '导出成功',
                    f'密码已成功导出到:\n{file_path}\n\n注意：导出文件已加密，只能通过本程序导入。'
                )
            else:
                QMessageBox.critical(self.parent_window, '导出失败', '导出密码时发生错误，请重试。')

    def import_passwords(self):
        """导入密码"""
        file_path, _ = QFileDialog.getOpenFileName(
            self.parent_window,
            '导入密码',
            '',
            'SecretBook文件 (*.sbk);;所有文件 (*)'
        )

        if file_path:
            # 询问导入模式
            reply = QMessageBox.question(
                self.parent_window,
                '导入模式',
                '请选择导入模式：\n\n'
                '• 点击"Yes"：合并模式（保留现有密码，添加新密码）\n'
                '• 点击"No"：替换模式（清空现有密码，仅保留导入的密码）\n'
                '• 点击"Cancel"：取消导入',
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                QMessageBox.Yes
            )

            if reply == QMessageBox.Cancel:
                return

            merge_mode = (reply == QMessageBox.Yes)

            # 执行导入
            success, message, duplicates = self.data_manager.import_passwords(file_path, merge_mode)

            if success:
                if duplicates:
                    # 处理重复密码
                    self.handle_duplicate_passwords(duplicates)
                else:
                    QMessageBox.information(self.parent_window, '导入成功', message)

                # 发射信号通知主窗口刷新
                self.passwords_updated.emit()
            else:
                QMessageBox.critical(self.parent_window, '导入失败', message)

    def handle_duplicate_passwords(self, duplicates: list):
        """处理重复密码"""
        for i, duplicate in enumerate(duplicates):
            import_data = duplicate['import_data']
            existing_data = duplicate['existing_data']

            reply = QMessageBox.question(
                self.parent_window,
                f'重复密码 ({i + 1}/{len(duplicates)})',
                f'发现重复密码：\n\n'
                f'应用名：{import_data.get("website", "")}\n'
                f'用户名：{import_data.get("username", "")}\n\n'
                f'现有密码：{existing_data.get("password", "")}\n'
                f'导入密码：{import_data.get("password", "")}\n\n'
                f'是否用导入的密码覆盖现有密码？',
                QMessageBox.Yes | QMessageBox.No | QMessageBox.YesToAll | QMessageBox.NoToAll,
                QMessageBox.No
            )

            if reply == QMessageBox.YesToAll:
                # 覆盖所有剩余重复项
                for remaining_duplicate in duplicates[i:]:
                    self.data_manager.update_password(
                        remaining_duplicate['existing_data']['id'],
                        remaining_duplicate['import_data'],
                        force_update=True
                    )
                break
            elif reply == QMessageBox.NoToAll:
                # 跳过所有剩余重复项
                break
            elif reply == QMessageBox.Yes:
                # 覆盖当前项
                self.data_manager.update_password(
                    existing_data['id'],
                    import_data,
                    force_update=True
                )
            # reply == QMessageBox.No 则跳过当前项