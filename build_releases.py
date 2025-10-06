#!/usr/bin/env python3
"""
PyInstallerを使用してマルチプラットフォームの実行ファイルを作成し、
配布用のZIPファイルを生成するスクリプト
"""

import os
import sys
import shutil
import zipfile
import platform
import subprocess


# 設定
PROJECT_NAME = "mosaic_tool"
SCRIPT_PATH = "src/mosaic_tool.py"
REQUIREMENTS_PATH = "src/requirements.txt"
README_PATH = "README.md"

# 出力ディレクトリ
BIN_DIRS = {
    "windows": "bin_win",
    "macos": "bin_mac", 
    "linux": "bin_linux"
}

# 現在のプラットフォーム
CURRENT_PLATFORM = platform.system().lower()
if CURRENT_PLATFORM == "darwin":
    CURRENT_PLATFORM = "macos"


def check_requirements():
    """必要なファイルとツールの存在を確認"""
    print("📋 必要な要件をチェック中...")
    
    # PyInstallerがインストールされているかチェック
    try:
        import PyInstaller
        print(f"✅ PyInstaller {PyInstaller.__version__} がインストールされています")
    except ImportError:
        print("❌ PyInstallerがインストールされていません")
        print("   pip install pyinstaller でインストールしてください")
        return False
    
    # 必要なファイルの存在確認
    required_files = [SCRIPT_PATH, REQUIREMENTS_PATH, README_PATH]
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"❌ 必要なファイルが見つかりません: {file_path}")
            return False
        print(f"✅ {file_path} が見つかりました")
    
    return True


def install_dependencies():
    """依存関係をインストール"""
    print("📦 依存関係をインストール中...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", REQUIREMENTS_PATH], 
                      check=True, capture_output=True, text=True)
        print("✅ 依存関係のインストールが完了しました")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依存関係のインストールに失敗しました: {e}")
        return False


def create_executable(platform_name):
    """指定されたプラットフォーム用の実行ファイルを作成"""
    print(f"🔨 {platform_name} 用の実行ファイルを作成中...")
    
    bin_dir = BIN_DIRS[platform_name]
    
    # 出力ディレクトリをクリーンアップ
    if os.path.exists(bin_dir):
        shutil.rmtree(bin_dir)
    os.makedirs(bin_dir, exist_ok=True)
    
    # PyInstallerのコマンドを構築
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # 単一の実行ファイルを作成
        "--windowed",  # コンソールウィンドウを表示しない（GUI用）
        "--name", PROJECT_NAME,
        "--distpath", bin_dir,
        "--workpath", f"build_{platform_name}",
        "--specpath", "build",
        SCRIPT_PATH
    ]
    
    # Windowsの場合、アイコンを追加（アイコンファイルがあれば）
    if platform_name == "windows" and os.path.exists("icon.ico"):
        cmd.extend(["--icon", "icon.ico"])
    
    try:
        # PyInstallerを実行
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {platform_name} 用の実行ファイルが作成されました")
        
        # README.mdをコピー
        shutil.copy2(README_PATH, bin_dir)
        print(f"✅ README.mdを {bin_dir} にコピーしました")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ {platform_name} 用の実行ファイル作成に失敗しました")
        print(f"   エラー: {e}")
        if e.stderr:
            print(f"   詳細: {e.stderr}")
        return False


def create_zip_archive(platform_name):
    """配布用のZIPファイルを作成"""
    print(f"📦 {platform_name} 用のZIPアーカイブを作成中...")
    
    bin_dir = BIN_DIRS[platform_name]
    zip_filename = f"{PROJECT_NAME}_{platform_name}.zip"
    
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # bin_dirの内容をZIPに追加
            for root, _, files in os.walk(bin_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # ZIP内のパスを調整
                    arcname = os.path.relpath(file_path, bin_dir)
                    zipf.write(file_path, arcname)
        
        print(f"✅ {zip_filename} が作成されました")
        return True
        
    except (OSError, zipfile.BadZipFile) as e:
        print(f"❌ ZIPアーカイブの作成に失敗しました: {e}")
        return False


def cleanup_build_files():
    """ビルドファイルをクリーンアップ"""
    print("🧹 ビルドファイルをクリーンアップ中...")
    
    cleanup_dirs = ["build", "dist"]
    for platform_name in BIN_DIRS.keys():
        cleanup_dirs.append(f"build_{platform_name}")
    
    for dir_name in cleanup_dirs:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ {dir_name} を削除しました")
    
    # .specファイルも削除
    spec_files = [f"{PROJECT_NAME}.spec"]
    for spec_file in spec_files:
        if os.path.exists(spec_file):
            os.remove(spec_file)
            print(f"✅ {spec_file} を削除しました")


def build_for_platform(platform_name):
    """指定されたプラットフォーム用のビルドを実行"""
    print(f"\n🚀 {platform_name.upper()} 用のビルドを開始...")
    
    if not create_executable(platform_name):
        return False
    
    if not create_zip_archive(platform_name):
        return False
    
    print(f"✅ {platform_name.upper()} 用のビルドが完了しました")
    return True


def main():
    """メイン関数"""
    print("🔧 Mosaic Tool - マルチプラットフォームビルドスクリプト")
    print("=" * 60)
    
    # 要件チェック
    if not check_requirements():
        sys.exit(1)
    
    # 依存関係のインストール
    if not install_dependencies():
        sys.exit(1)
    
    # ビルド対象のプラットフォーム
    if len(sys.argv) > 1:
        # コマンドライン引数でプラットフォームを指定
        target_platforms = []
        for arg in sys.argv[1:]:
            if arg in BIN_DIRS:
                target_platforms.append(arg)
            else:
                print(f"⚠️  不明なプラットフォーム: {arg}")
                print(f"   利用可能なプラットフォーム: {list(BIN_DIRS.keys())}")
    else:
        # 現在のプラットフォーム用のみビルド
        target_platforms = [CURRENT_PLATFORM]
        print(f"ℹ️  現在のプラットフォーム ({CURRENT_PLATFORM}) 用にビルドします")
        print("   全プラットフォーム用にビルドする場合:")
        print("   python build_releases.py windows macos linux")
    
    success_count = 0
    total_count = len(target_platforms)
    
    # 各プラットフォーム用にビルド
    for platform_name in target_platforms:
        if build_for_platform(platform_name):
            success_count += 1
        else:
            print(f"❌ {platform_name} 用のビルドに失敗しました")
    
    # ビルドファイルのクリーンアップ
    cleanup_build_files()
    
    # 結果の表示
    print("\n" + "=" * 60)
    print(f"🎉 ビルド完了: {success_count}/{total_count} プラットフォーム")
    
    if success_count > 0:
        print("\n📁 作成されたファイル:")
        for platform_name in target_platforms:
            bin_dir = BIN_DIRS[platform_name]
            zip_file = f"{PROJECT_NAME}_{platform_name}.zip"
            if os.path.exists(bin_dir):
                print(f"   📂 {bin_dir}/")
            if os.path.exists(zip_file):
                print(f"   📦 {zip_file}")
        
        print("\n✨ 配布用ZIPファイルが作成されました！")
    
    if success_count < total_count:
        sys.exit(1)


if __name__ == "__main__":
    main()