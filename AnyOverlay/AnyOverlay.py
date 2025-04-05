import threading
from gui import tray
from gui import overlay
from gui import settings

def main():
    # 設定
    st = settings.Settings()
    # オーバーレイ
    ol = overlay.Overlay(st)
    # タスクトレイ
    tt = tray.TaskTray(ol)

    # タスクトレイ処理をサブスレッドで実行
    threading.Thread(target=tt.tray_thread, daemon=True).start()

    # Webviewをメインスレッドで実行
    ol.start_webview()

if __name__ == '__main__':
    main()
