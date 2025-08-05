#!/bin/bash

echo "=== 產品生成器安裝腳本 ==="

# 檢查 Python 版本
python_version=$(python3 --version 2>&1)
echo "Python 版本: $python_version"

# 創建虛擬環境
echo "創建虛擬環境..."
python3 -m venv venv

# 激活虛擬環境
echo "激活虛擬環境..."
source venv/bin/activate

# 安裝依賴
echo "安裝依賴..."
pip install -r requirements.txt

# 創建必要的目錄
echo "創建目錄結構..."
mkdir -p product-packages
mkdir -p src/_data/content/products/details
mkdir -p static/assets/images/product

# 設置權限
echo "設置文件權限..."
chmod +x package_watcher.py
chmod +x page_generator.py
chmod +x start_watcher.py

echo "=== 安裝完成 ==="
echo ""
echo "下一步："
echo "1. 設置 OpenAI API Key:"
echo "   export OPENAI_API_KEY='your-api-key'"
echo ""
echo "2. 啟動系統:"
echo "   source venv/bin/activate"
echo "   python start_watcher.py"
echo ""
echo "3. 將產品包放入 product-packages/ 目錄" 