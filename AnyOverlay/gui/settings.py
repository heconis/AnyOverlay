import json
import os

class Settings:
    def __init__(self, settings_file='/settings.json'):
        # 設定ディレクトリの存在確認 & 作成
        dir_path = os.path.join(os.getenv('LocalAppData'), 'AnyOverlay')
        os.makedirs(dir_path, exist_ok=True)
        self.settings_file = dir_path + settings_file
        self.window_size = {'width': 480, 'height': 360}
        self.window_pos = {'x': 100, 'y': 100}
        self.url = ''
        self.transparent = 90
        self.mouse_through = False
        self.ret = self.load()

    def load(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                    self.window_size = data.get('window_size')
                    self.window_pos = data.get('window_pos')
                    self.url = data.get('url')
                    self.transparent = data.get('transparent')
                    self.mouse_through = data.get('mouse_through')
                    return True
                except json.JSONDecodeError:
                    print("設定ファイルの読み込みに失敗しました。")
                    return False
        else:
            print(f"{self.settings_file} が見つかりません。デフォルト設定を使用します。")
            return False

    def save(self):
        data = {
            'window_size': self.window_size,
            'window_pos': self.window_pos,
            'url': self.url,
            'transparent': self.transparent,
            'mouse_through' : self.mouse_through
        }
        with open(self.settings_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

