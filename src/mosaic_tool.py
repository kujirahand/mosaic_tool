"""モザイク専用ツール"""

from PIL import Image
import TkEasyGUI as eg

# 定数の宣言
CANVAS_SIZE = (800, 600)  # キャンバスのサイズ
MOSAIC_SIZE = 5  # モザイクのサイズ（タイポ修正）


# グローバル変数をクラスで管理
class AppState:
    """アプリケーションの状態を管理するクラス"""

    def __init__(self):
        self.is_mouse_down = False
        self.start_pos = (0, 0)  # 変数名を変更
        self.move_list = []
        self.canvas_img = None  # キャンバスに表示する画像
        self.original_img = None  # 元画像
        self.rate = 1.0  # 画像の拡大率


# グローバルなアプリケーション状態
app_state = AppState()


def main():
    """メイン関数"""
    # 最初に画像ファイルを選択
    fname = eg.popup_get_file(
        "画像ファイルを選択してください",
        file_types=(("Image Files", "*.png;*.jpg;*.jpeg;*.gif"),),
    )
    if fname is None or fname == "":
        eg.popup_ok("画像ファイルが選択されませんでした")
        return
    # 画像をウィンドウに合うようにリサイズ
    app_state.canvas_img = Image.open(fname)
    app_state.original_img = app_state.canvas_img.copy()
    org_size = app_state.canvas_img.size
    app_state.canvas_img.thumbnail(CANVAS_SIZE)
    app_state.rate = org_size[0] / app_state.canvas_img.size[0]
    # ウィンドウを表示
    show_window()


# モザイクを掛ける処理
def mosaic(img, start_coords, end_coords, size=MOSAIC_SIZE):
    """モザイク処理を行う関数"""
    x0, y0 = start_coords
    x1, y1 = end_coords
    region = img.crop((x0, y0, x1, y1))
    region = region.resize(
        ((x1 - x0) // int(size), (y1 - y0) // int(size)), Image.Resampling.NEAREST
    )
    region = region.resize((x1 - x0, y1 - y0), Image.Resampling.NEAREST)
    img.paste(region, (x0, y0, x1, y1))
    return img


def mosaic_x2(cv_img, org_img, start_coords, end_coords, size):
    """画面画像とオリジナル画像の二つにモザイク処理を行う関数"""
    # 画面画像にモザイクを掛ける
    cv_img = mosaic(cv_img, start_coords, end_coords, size=size)
    # 元画像にもモザイクを掛けておく
    sx0, sy0 = int(start_coords[0] * app_state.rate), int(
        start_coords[1] * app_state.rate
    )
    sx1, sy1 = int(end_coords[0] * app_state.rate), int(end_coords[1] * app_state.rate)
    org_img = mosaic(org_img, (sx0, sy0), (sx1, sy1), size=int(size * app_state.rate))


def show_window():
    """メインウィンドウを表示する関数"""
    # 変数を初期化
    canvas = eg.Graph(key="-cv", canvas_size=CANVAS_SIZE)  # キャンバス作成
    # メインウィンドウを作成
    window = eg.Window(
        "画像表示",
        layout=[
            [canvas],  # キャンバスを配置
            [eg.HSeparator()],
            [
                eg.Push(),
                eg.Text("モザイクサイズ:"),
                eg.Slider(
                    range=(2, 50), key="-ms", orientation="h", default_value=MOSAIC_SIZE
                ),
                eg.Button("保存"),
                eg.Button("終了"),
            ],
        ],
    )
    # マウスイベントをバインド
    canvas.bind_events(
        {
            "<ButtonPress>": "mousedown",
            "<ButtonRelease>": "mouseup",
            "<Motion>": "mousemove",
        },
        "system",
    )
    # 初期画像を描画
    canvas.draw_image(location=(0, 0), data=app_state.canvas_img)
    # イベントループ
    while window.is_alive():
        event, values = window.read()
        if event == "-cv":  # キャンバスのイベント
            handle_mouse_event(window, values)
        elif event == "@drawing":  # 画面描画イベント
            if len(app_state.move_list) == 0:
                continue
            x, y = app_state.move_list.pop(0)
            if len(app_state.move_list) > 0:
                continue  # 最新の座標だけ描画するように調整
            canvas.draw_image(
                location=(0, 0), data=app_state.canvas_img
            )  # 画像を再描画
            canvas.draw_rectangle(
                app_state.start_pos, (x, y), line_color="blue", line_width=3
            )
        elif event == "保存":  # オリジナル画像を保存
            fname = eg.popup_get_file(
                "保存先のファイル名を指定してください",
                save_as=True,
                default_extension=".png",
            )
            if fname is not None and fname != "":
                app_state.original_img.save(fname)
                eg.popup_ok("保存しました")
        elif event == "終了":
            if eg.popup_yes_no("終了してもよろしいですか？") == "Yes":
                break
    window.close()

def handle_mouse_event(window, values):
    """マウスイベントを処理する関数"""
    # マウスイベントの種類と位置を取得
    event_type = values["event_type"] if "event_type" in values else ""
    event = values["event"] if "event" in values else {"x": 0, "y": 0}
    if event_type == "mousedown":  # マウスボタンを押したとき
        app_state.is_mouse_down = True
        app_state.start_pos = (event.x, event.y)
    elif event_type == "mousemove" and app_state.is_mouse_down:  # マウスが動いたとき
        app_state.move_list.append((event.x, event.y))
        window.post_event_after(1, "@drawing", {})  # 1ms後に描画イベントを発生
    elif event_type == "mouseup":  # マウスボタンを離したとき
        app_state.is_mouse_down = False
        w, h = (event.x - app_state.start_pos[0], event.y - app_state.start_pos[1])
        if w < 0 or h < 0:
            return
        mosaic_size = values["-ms"] if "-ms" in values else MOSAIC_SIZE
        mosaic_x2(
            app_state.canvas_img,
            app_state.original_img,
            app_state.start_pos,
            (event.x, event.y),
            mosaic_size,
        )
        window["-cv"].draw_image(location=(0, 0), data=app_state.canvas_img)
        app_state.move_list = []


if __name__ == "__main__":
    main()
