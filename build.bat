@echo off
REM Windows用のビルドスクリプト

echo 🔧 Mosaic Tool - ビルドスクリプト (Windows)
echo ==============================================

REM PyInstallerをインストール
echo 📦 PyInstallerをインストール中...
pip install pyinstaller

REM ビルドスクリプトを実行
python build_releases.py

echo ✅ ビルド完了！
pause