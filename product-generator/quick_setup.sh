#!/bin/bash

echo "=== 產品生成器快速設置 ==="

# 檢查是否在正確的目錄
if [ ! -f "package_watcher.py" ]; then
    echo "❌ 請在 product-generator 目錄中運行此腳本"
    exit 1
fi

# 創建虛擬環境
echo "📦 創建虛擬環境..."
python3 -m venv venv

# 激活虛擬環境
echo "🔧 激活虛擬環境..."
source venv/bin/activate

# 安裝依賴
echo "📥 安裝依賴..."
pip install -r requirements.txt

# 創建目錄
echo "📁 創建目錄結構..."
mkdir -p product-packages
mkdir -p src/_data/content/products/details
mkdir -p static/assets/images/product

# 設置權限
echo "🔐 設置文件權限..."
chmod +x package_watcher.py
chmod +x page_generator.py
chmod +x start_watcher.py
chmod +x setup_api_key.py

# 創建配置文件模板
echo "⚙️ 創建配置文件模板..."
python3 config.py

echo ""
echo "✅ 安裝完成！"
echo ""
echo "下一步：設置 API Key"
echo "運行: python setup.py"
echo ""
echo "或者手動編輯: product-generator/config.json"
echo ""
echo "設置完成後，啟動系統："
echo "source venv/bin/activate"
echo "python start_watcher.py" 