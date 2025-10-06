#!/bin/bash
# macOS/Linux用のビルドスクリプト

echo "🔧 Mosaic Tool - ビルドスクリプト (macOS/Linux)"
echo "================================================="

# PyInstallerをインストール
echo "📦 PyInstallerをインストール中..."
pip install pyinstaller

# ビルドスクリプトを実行
python build_releases.py

echo "✅ ビルド完了！"