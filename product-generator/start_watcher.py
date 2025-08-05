#!/usr/bin/env python3
"""
Product Generator Startup Script
啟動產品生成器的完整工作流程
"""

import os
import sys
from pathlib import Path

# 添加當前目錄到 Python 路徑
sys.path.append(str(Path(__file__).parent))

from package_watcher import ProductPackageHandler
from page_generator import PageGenerator

def setup_environment():
    """設置環境"""
    # 創建必要的目錄
    directories = [
        'product-packages',
        'src/_data/content/products/details',
        'static/assets/images/product',
        'src/en/products',
        'src/de/products'
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"確保目錄存在: {dir_path}")

def check_dependencies():
    """檢查依賴"""
    try:
        import watchdog
        import openai
        import yaml
        print("✓ 所有依賴已安裝")
        return True
    except ImportError as e:
        print(f"✗ 缺少依賴: {e}")
        print("請運行: pip install -r requirements.txt")
        return False

def check_api_key():
    """檢查 API Key"""
    from config import check_api_key as check_config_api_key
    return check_config_api_key()

def main():
    """主函數"""
    print("=== 產品生成器啟動 ===")
    
    # 檢查環境
    if not check_dependencies():
        return
    
    if not check_api_key():
        return
    
    # 設置環境
    setup_environment()
    
    # 讀取配置
    from config import get_config
    config = get_config()
    if not config:
        print("❌ 無法讀取配置文件")
        return
    
    print("\n=== 系統已準備就緒 ===")
    print("使用說明:")
    print("1. 將產品包（ZIP 文件）放入 product-packages/ 目錄")
    print("2. 系統會自動檢測並處理")
    print("3. 生成的 YAML 文件會保存到 src/_data/content/products/details/")
    print("4. 圖片會移動到 static/assets/images/product/")
    print("5. 頁面文件會自動生成")
    print("\n按 Ctrl+C 停止監控")
    
    # 啟動監控
    from package_watcher import main as start_watcher
    start_watcher()

if __name__ == "__main__":
    main() 