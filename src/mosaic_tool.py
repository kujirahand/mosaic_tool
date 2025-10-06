"""モザイク専用ツール"""
from PIL import Image
import TkEasyGUI as eg

# 定数の宣言
CANVAS_SIZE = (800, 600)  # キャンバスのサイズ
MOSIC_SIZE = 5 # モザイクのサイズ
# グローバル変数
is_mouse_down = False
start_xy = (0, 0)
move_list = []
canvas_img = None  # キャンバスに表示する画像
original_img = None  # 元画像
rate = 1.0  # 画像の拡大率

def main():
    """メイン関数"""
    global canvas_img, original_img, rate
    # 最初に画像ファイルを選択
    fname = eg.popup_get_file("画像ファイルを選択してください",
                file_types=(("Image Files", "*.png;*.jpg;*.jpeg;*.gif"),))
    if fname is None or fname == "":
        eg.popup_ok("画像ファイルが選択されませんでした")
        exit()
    # 画像をウィンドウに合うようにリサイズ
    canvas_img = Image.open(fname)
    original_img = canvas_img.copy()
    org_size = canvas_img.size
    canvas_img.thumbnail(CANVAS_SIZE)
    rate = org_size[0] / canvas_img.size[0]
    # ウィンドウを表示
    show_window()

# モザイクを掛ける処理
def mosaic(img, start_xy, end_xy, size=MOSIC_SIZE):
    """モザイク処理を行う関数"""
    x0, y0 = start_xy
    x1, y1 = end_xy
    region = img.crop((x0, y0, x1, y1))
    region = region.resize(
        ((x1 - x0) // int(size), (y1 - y0) // int(size)),
        Image.NEAREST
    )
    region = region.resize((x1 - x0, y1 - y0), Image.NEAREST)
    img.paste(region, (x0, y0, x1, y1))
    return img

def mosaic_x2(cv_img, org_img, start_xy, end_xy, size):
    """画面画像とオリジナル画像の二つにモザイク処理を行う関数"""
    # 画面画像にモザイクを掛ける
    cv_img = mosaic(cv_img, start_xy, end_xy, size=size)
    # 元画像にもモザイクを掛けておく
    sx0, sy0 = int(start_xy[0] * rate), int(start_xy[1] * rate)
    sx1, sy1 = int(end_xy[0] * rate), int(end_xy[1] * rate)
    org_img = mosaic(org_img, (sx0, sy0), (sx1, sy1), size=int(size * rate))

def show_window():
    """メインウィンドウを表示する関数"""
    # 変数を初期化
    canvas = eg.Graph(key="-cv", canvas_size=CANVAS_SIZE)  # キャンバス作成
    # メインウィンドウを作成
    window = eg.Window("画像表示", layout=[
        [canvas],  # キャンバスを配置
        [eg.HSeparator()],
        [
            eg.Push(), eg.Text("モザイクサイズ:"),
            eg.Slider(range=(2, 50), key="-ms", orientation="h", default_value=MOSIC_SIZE),
            eg.Button("保存"), eg.Button("終了")
        ],
    ])
    # マウスイベントをバインド
    canvas.bind_events({
        "<ButtonPress>": "mousedown",
        "<ButtonRelease>": "mouseup",
        "<Motion>": "mousemove"
    }, "system")
    # 初期画像を描画
    canvas.draw_image(location=(0, 0), data=canvas_img)
    # イベントループ
    while window.is_alive():
        event, values = window.read()
        if event == "-cv":  # キャンバスのイベント
            handle_mouse_event(window, values)
        elif event == "@drawing":  # 画面描画イベント
            if len(move_list) == 0:
                continue
            x, y = move_list.pop(0)
            if len(move_list) > 0:
                continue  # 最新の座標だけ描画するように調整
            canvas.draw_image(location=(0, 0), data=canvas_img)  # 画像を再描画
            canvas.draw_rectangle(start_xy, (x, y), line_color="blue", line_width=3)
        elif event == "保存":  # オリジナル画像を保存
            fname = eg.popup_get_file("保存先のファイル名を指定してください", save_as=True,
                        default_extension=".png")
            if fname is not None or fname != "":
                original_img.save(fname)
                eg.popup_ok("保存しました")
        elif event == "終了":
            break

def handle_mouse_event(window, values):
    """マウスイベントを処理する関数"""
    global is_mouse_down, start_xy, move_list
    # マウスイベントの種類と位置を取得
    event_type = values["event_type"] if "event_type" in values else ""
    event = values["event"] if "event" in values else {"x": 0, "y": 0}
    if event_type == "mousedown":  # マウスボタンを押したとき
        is_mouse_down = True
        start_xy = (event.x, event.y)
    elif event_type == "mousemove" and is_mouse_down:  # マウスが動いたとき
        move_list.append((event.x, event.y))
        window.post_event_after(1, "@drawing", {})  # 1ms後に描画イベントを発生
    elif event_type == "mouseup":  # マウスボタンを離したとき
        is_mouse_down = False
        w, h = (event.x - start_xy[0], event.y - start_xy[1])
        if w < 0 or h < 0:
            return
        mosaic_size = values["-ms"] if "-ms" in values else MOSIC_SIZE
        mosaic_x2(canvas_img, original_img, start_xy, (event.x, event.y), mosaic_size)
        window["-cv"].draw_image(location=(0, 0), data=canvas_img)
        move_list = []

if __name__ == "__main__":
    main()
