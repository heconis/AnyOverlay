import time
import webview

import win32api
import win32con
import win32gui

class Api:
    overlay = None
    def __init__(self, ol):
        global overlay
        overlay = ol
        
    def file_select(self):
        file_path = overlay.setting_window.create_file_dialog(dialog_type=webview.OPEN_DIALOG)[0]
        return file_path

    def change_mouse_through(self, flg):
        overlay.settings.mouse_through = flg
        overlay.set_click_through(flg)

    def change_transarent(self, val):
        overlay.settings.transparent = val
        overlay.set_transparent(val)
        return False
    
    def save(self, url):
        overlay.settings.url = url
        overlay.set_url(url)

    def close(self):
        overlay.save()
        overlay.setting_window.destroy()
        
class Overlay:
    def __init__(self, settings):
        # 設定
        self.settings = settings
        # ウィンドウの初期設定
        webview.settings['ALLOW_FILE_URLS'] = True
        webview.DRAG_REGION_SELECTOR = 'body:not(.drag-disabled), header'
        self.window = webview.create_window(
            title='AnyOverlay',
            url=self.settings.url,
            width=self.settings.window_size['width'],
            height=self.settings.window_size['height'],
            x=self.settings.window_pos['x'],
            y=self.settings.window_pos['y'],
            easy_drag=True,
            on_top=True
        )
        # 設定表示状態
        self.is_setting_open = False

    # 設定値を保存する
    def save(self):
        self.settings.window_size = {'width': self.window.width, 'height': self.window.height}
        self.settings.window_pos = {'x': self.window.x, 'y': self.window.y}
        self.settings.save()

    # 透過度を更新する
    def set_transparent(self, val):
        try:
            time.sleep(0.01)
            win32gui.SetLayeredWindowAttributes(self.hWnd, win32api.RGB(0,0,0), int(255*(val/100)), win32con.LWA_ALPHA | win32con.LWA_COLORKEY)
        except:
            pass

    # ウィンドウリサイズ可否設定
    def set_resizable_window(self, is_resizable):
        try:
            time.sleep(0.01)
            style = win32api.GetWindowLong(self.hWnd, win32con.GWL_STYLE)
            if is_resizable:
                style = style | win32con.WS_THICKFRAME
            else:
                style = style & ~win32con.WS_OVERLAPPEDWINDOW
            win32api.SetWindowLong(self.hWnd, win32con.GWL_STYLE, style)
            win32gui.SetWindowPos(self.hWnd, None, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_FRAMECHANGED)
        except:
            pass

    # ウィンドウクリック可否設定
    def set_click_through(self, is_through):
        try:
            time.sleep(0.01)
            style = win32gui.GetWindowLong(self.hWnd, win32con.GWL_EXSTYLE)
            if is_through:
                style = style | win32con.WS_EX_TRANSPARENT
            else:
                style = style & ~win32con.WS_EX_TRANSPARENT
            win32gui.SetWindowLong(self.hWnd, win32con.GWL_EXSTYLE, style)
        except:
            pass
    
    # urlを更新する
    def set_url(self, url):
        self.window.load_url(url)

    # ウィンドウ読込後実行関数
    def on_loaded(self):
        self.window.restore()
        self.hWnd = win32gui.FindWindow(None, 'AnyOverlay')
        exStyle = win32gui.GetWindowLong(self.hWnd, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(self.hWnd, win32con.GWL_EXSTYLE, exStyle | win32con.WS_EX_LAYERED)
        self.set_resizable_window(False)
        self.set_click_through(self.settings.mouse_through)
        self.set_transparent(self.settings.transparent)
        if self.settings.url == '': self.view_setting()

    # ウィンドウ終了
    def on_close(self):
        self.settings.save()
        if hasattr(self, 'setting_window'): self.setting_window.destroy()
        self.window.destroy()

    def on_closed(self):
        self.window.restore()
        self.set_resizable_window(False)
        self.is_setting_open = False

    # 設定ウィンドウを表示
    def view_setting(self):
        self.is_setting_open = True
        with open('assets/index.html', 'r', encoding='utf-8') as file:
            api = Api(self)
            self.setting_window = webview.create_window(
                title='Settings',
                html=file.read(),
                width=400,
                height=325,
                frameless=True,
                easy_drag=True,
                on_top=True,
                js_api=api
            )
        self.setting_window.dom.get_element('#url').value = self.settings.url
        self.setting_window.dom.get_element('#opacity').value = self.settings.transparent
        self.setting_window.dom.get_element('#opacity-value').text = self.settings.transparent
        self.setting_window.evaluate_js(f"document.querySelector('#ignore-mouse').checked = {'true' if self.settings.mouse_through else 'false'};")
        self.setting_window.events.closed += self.on_closed
        self.set_resizable_window(True)
        self.set_click_through(False)

    # Webview表示の関数
    def start_webview(self):
        webview.start(self.on_loaded, private_mode=False, http_server=True)
