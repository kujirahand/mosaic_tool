# ビルドガイド - Mosaic Tool

このディレクトリには、Mosaic Toolをマルチプラットフォーム用の実行ファイルとして配布するためのビルドスクリプトが含まれています。

## 必要な環境

- Python 3.7以上
- pip
- インターネット接続（PyInstallerのインストール用）

## 簡単なビルド方法

### macOS/Linux の場合
```bash
./build.sh
```

### Windows の場合
```cmd
build.bat
```

## 手動ビルド方法

### 1. PyInstallerをインストール
```bash
pip install pyinstaller
```

### 2. ビルドスクリプトを実行

#### 現在のプラットフォーム用のみ
```bash
python build_releases.py
```

#### 特定のプラットフォーム用
```bash
# Windows用
python build_releases.py windows

# macOS用  
python build_releases.py macos

# Linux用
python build_releases.py linux

# 複数プラットフォーム用
python build_releases.py windows macos linux
```

## 出力ファイル

ビルドが成功すると、以下のファイルとディレクトリが作成されます：

### ディレクトリ
- `bin_win/` - Windows用実行ファイルとREADME.md
- `bin_mac/` - macOS用実行ファイルとREADME.md  
- `bin_linux/` - Linux用実行ファイルとREADME.md

### ZIPファイル（配布用）
- `mosaic_tool_windows.zip` - Windows用配布パッケージ
- `mosaic_tool_macos.zip` - macOS用配布パッケージ
- `mosaic_tool_linux.zip` - Linux用配布パッケージ

## スクリプトの機能

`build_releases.py`スクリプトは以下の処理を自動的に行います：

1. **環境チェック** - PyInstallerと必要なファイルの存在確認
2. **依存関係インストール** - requirements.txtに基づく自動インストール
3. **実行ファイル作成** - PyInstallerによる単一実行ファイルの生成
4. **ファイル配置** - README.mdの各ディレクトリへのコピー
5. **ZIP圧縮** - 配布用ZIPファイルの作成
6. **クリーンアップ** - 一時ビルドファイルの削除

## トラブルシューティング

### PyInstallerのインストールエラー
```bash
# アップグレードを試してください
pip install --upgrade pip
pip install pyinstaller
```

### ビルドエラー
```bash
# 依存関係を再インストール
pip install -r src/requirements.txt
```

### 権限エラー（macOS/Linux）
```bash
chmod +x build.sh
```

## 注意事項

- クロスプラットフォームビルドは各プラットフォーム上で実行する必要があります
- Windows用実行ファイルはWindows上でのみ作成可能です
- macOS用実行ファイルはmacOS上でのみ作成可能です
- Linux用実行ファイルはLinux上でのみ作成可能です

## カスタマイズ

`build_releases.py`の設定を変更することで、以下をカスタマイズできます：

- プロジェクト名（`PROJECT_NAME`）
- 出力ディレクトリ名（`BIN_DIRS`）
- PyInstallerのオプション（`cmd`リスト内）
- アイコンファイルの指定（icon.icoがある場合）

## 配布方法

作成されたZIPファイルをユーザーに配布してください：

1. 適切なプラットフォーム用のZIPファイルをダウンロード
2. ZIPファイルを展開
3. 実行ファイル（mosaic_tool）を実行
4. README.mdで使用方法を確認