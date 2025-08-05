# 產品自動生成器

這是一個自動化的產品生成系統，使用 OpenAI GPT-4.1-mini 來處理產品文本並生成結構化的 YAML 數據。

## 功能特點

- 🔍 **自動監控**: 監控 `product-packages` 目錄，自動處理新的產品包
- 🤖 **AI 處理**: 使用 GPT-4.1-mini 智能解析產品文本
- 🌐 **多語言支援**: 自動生成英文和德文版本
- 📁 **文件管理**: 自動處理圖片和創建頁面文件
- ⚙️ **配置更新**: 自動更新 Eleventy 配置

## 安裝和設置

### 1. 安裝依賴
```bash
cd product-generator
pip install -r requirements.txt
```

### 2. 設置 OpenAI API Key

#### 方法 1: 使用設置腳本（推薦）
```bash
python setup.py
```

#### 方法 2: 手動編輯配置文件
編輯 `product-generator/config.json` 文件：
```json
{
  "openai_api_key": "your-api-key-here",
  "packages_dir": "product-packages",
  "output_dir": "src/_data/content/products/details",
  "images_dir": "static/assets/images/product",
  "model": "gpt-4o-mini",
  "temperature": 0.3,
  "max_tokens": 2000
}
```

### 3. 啟動系統
```bash
python start_watcher.py
```

## 產品包格式

### ZIP 文件結構
```
product-name.zip
├── spec.md              # 產品規格文本（必需）
├── images/              # 產品圖片目錄（可選）
│   ├── product-1.jpg
│   ├── product-2.jpg
│   └── feature-1.jpg
└── metadata.json        # 額外信息（可選）
```

### 規格文件範例 (spec.md)
```markdown
產品名稱
產品標語
產品描述

特色 1
特色描述

特色 2
特色描述

技術規格
容量    256GB    512GB    1TB
讀取速度  3100MB/s  3370MB/s  3470MB/s
寫入速度  1040MB/s  2030MB/s  3000MB/s
```

## 工作流程

1. **準備產品包**: 創建包含產品文本和圖片的 ZIP 文件
2. **放入監控目錄**: 將 ZIP 文件放入 `product-packages/` 目錄
3. **自動處理**: 系統自動檢測並處理文件
4. **生成文件**: 自動生成 YAML 數據和頁面文件
5. **審核結果**: 檢查生成的文件並進行必要的修改

## 生成的文件

### YAML 數據文件
- `src/_data/content/products/details/[product-name]/en.yml`
- `src/_data/content/products/details/[product-name]/de.yml`

### 圖片文件
- `static/assets/images/product/[product-name]/`

### 頁面文件
- `src/en/products/[category]/[product-name]/index.njk`
- `src/de/products/[category]/[product-name]/index.njk`

## 配置選項

可以在 `start_watcher.py` 中修改以下配置：

```python
config = {
    'packages_dir': 'product-packages',           # 監控目錄
    'output_dir': 'src/_data/content/products/details',  # YAML 輸出目錄
    'images_dir': 'static/assets/images/product', # 圖片輸出目錄
    'openai_api_key': os.getenv('OPENAI_API_KEY')
}
```

## 錯誤處理

### 常見問題

1. **API Key 錯誤**
   - 確保正確設置 `OPENAI_API_KEY` 環境變數

2. **依賴缺失**
   - 運行 `pip install -r requirements.txt`

3. **文件格式錯誤**
   - 確保 ZIP 文件包含 `spec.md` 文件
   - 檢查文件編碼（建議使用 UTF-8）

4. **權限問題**
   - 確保腳本有寫入目標目錄的權限

## 自定義和擴展

### 修改 LLM 提示詞
在 `package_watcher.py` 中修改 `generate_yaml` 方法的 prompt 變數。

### 添加新的產品類別
在 `page_generator.py` 中修改 `determine_category` 方法。

### 自定義頁面模板
修改 `create_page_template` 方法來調整頁面結構。

## 最佳實踐

1. **產品文本準備**
   - 使用清晰的結構和格式
   - 包含完整的技術規格
   - 提供高質量的產品圖片

2. **文件命名**
   - 使用 kebab-case 命名產品包
   - 圖片文件名使用小寫字母和數字

3. **質量控制**
   - 始終審核生成的 YAML 文件
   - 檢查翻譯的準確性
   - 驗證頁面顯示效果

## 故障排除

### 日誌輸出
系統會輸出詳細的處理日誌，包括：
- 文件檢測
- 處理進度
- 錯誤信息

### 手動處理
如果自動處理失敗，可以：
1. 檢查錯誤日誌
2. 手動修改生成的 YAML 文件
3. 重新運行系統

## 支援

如有問題，請檢查：
1. 依賴是否正確安裝
2. API Key 是否有效
3. 文件格式是否正確
4. 目錄權限是否足夠 