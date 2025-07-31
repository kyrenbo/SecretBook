import os
import sys
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
            # 获取资源文件路径（兼容打包后的情况）
            if getattr(sys, 'frozen', False):
                # 打包后的情况
                base_path = sys._MEIPASS
            else:
                # 开发环境
                current_file = os.path.abspath(__file__)
                base_path = os.path.dirname(os.path.dirname(current_file))
            
            # 优先尝试 ICO 文件，然后是 SVG
            icon_files = ['app.ico', 'logo.svg', 'logo.png']
            
            for icon_file in icon_files:
                icon_path = os.path.join(base_path, 'assets', icon_file)
                if os.path.exists(icon_path):
                    print(f"找到图标文件: {icon_path}")
                    return QIcon(icon_path)
            
            print(f"未找到图标文件，搜索路径: {os.path.join(base_path, 'assets')}")
            # 列出 assets 目录内容进行调试
            assets_path = os.path.join(base_path, 'assets')
            if os.path.exists(assets_path):
                files = os.listdir(assets_path)
                print(f"assets 目录内容: {files}")
            
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
                print("窗口图标设置成功")
            else:
                print("图标为空，无法设置窗口图标")
        except Exception as e:
            print(f"设置窗口图标失败: {e}")