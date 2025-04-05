import threading
import pystray
from pystray import MenuItem as item
from PIL import Image

class TaskTray(threading.Thread):
    def __init__(self, overlay):
        super().__init__()
        self.overlay = overlay

    # タスクトレイのメニュー項目
    def on_quit(self, icon, item):
        self.overlay.on_close()
        icon.stop()

    def on_setting(self, icon, item):
        if not self.overlay.is_setting_open: self.overlay.view_setting()

    # タスクトレイのメニュー作成
    def setup_tray(self):
        icon = pystray.Icon('icon', Image.open('assets/icon.ico'), menu=(
            item('設定', self.on_setting, default=True),
            item('終了', self.on_quit)
        ))
        icon.run()

    # タスクトレイをサブスレッドで実行
    def tray_thread(self):
        self.setup_tray()