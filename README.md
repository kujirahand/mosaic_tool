# Mosaic Tool

シンプルなモザイク掛けツールです。

## インストールの方法

Clone the repository and install the required packages:

```sh
git clone https://github.com/kujirahand/mosaic_tool.git
cd mosaic_tool/src
pip install -r requirements.txt
```

## 使い方

Run the main script to start the GUI:

```sh
python mosaic_tool.py
```

画像ファイルを選ぶと編集画面がでます。マウスでモザイクを掛けたい範囲を選択してください。選択した範囲にモザイクが掛かります。

Select the image file, and select the mosaic area by dragging the mouse. The mosaic will be applied to the selected area.

## バイナリ配布版

事前にビルドされた実行ファイルをダウンロードして使用することもできます：

- Windows用: `mosaic_tool_windows.zip`
- macOS用: `mosaic_tool_macos.zip` 

ZIPファイルを展開して、実行ファイル（`mosaic_tool`）を実行してください。

## ビルド方法

開発者向け：実行ファイルを自分でビルドする場合は、以下のスクリプトを使用してください：

### 簡単な方法

```sh
# macOS/Linux
./build.sh

# Windows  
build.bat
```

### 詳細な方法

```sh
# PyInstallerをインストール
pip install pyinstaller

# 現在のプラットフォーム用
python build_releases.py

# 特定のプラットフォーム用
python build_releases.py windows macos linux
```

詳細については `BUILD_README.md` をご参照ください。

````
