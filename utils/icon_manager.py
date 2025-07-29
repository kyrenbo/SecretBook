import os
from PySide6.QtGui import QIcon

class IconManager:
    """图标管理器 - 统一管理应用程序图标"""
    
    _app_icon = None
    
    @classmethod
    def get_app_icon(cls) -> QIcon:
        """获取应用程序图标"""
        if cls._app_icon is None:
            cls._app_icon = cls._load_app_icon()
        return cls._app_icon
    
    @classmethod
    def _load_app_icon(cls) -> QIcon:
        """加载应用程序图标"""
        try:
            # 获取项目根目录
            current_file = os.path.abspath(__file__)
            project_root = os.path.dirname(os.path.dirname(current_file))
            logo_path = os.path.join(project_root, 'assets', 'logo.svg')
            
            if os.path.exists(logo_path):
                return QIcon(logo_path)
            else:
                print(f"Logo文件不存在: {logo_path}")
                return QIcon()  # 返回空图标
        except Exception as e:
            print(f"加载图标失败: {e}")
            return QIcon()  # 返回空图标
    
    @classmethod
    def set_window_icon(cls, window):
        """为窗口设置图标"""
        try:
            icon = cls.get_app_icon()
            if not icon.isNull():
                window.setWindowIcon(icon)
        except Exception as e:
            print(f"设置窗口图标失败: {e}")