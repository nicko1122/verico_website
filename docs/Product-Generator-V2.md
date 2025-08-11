### Product-Generator V2 操作手冊

本工具將產品資料包（ZIP）轉換為 11ty 網站可用的產品資料與資產：
- 解析 `product.md`（英文）為結構化 JSON
- 以 LLM 翻譯產出德文對應資料
- 依網站資料結構轉為 YAML：`src/_data/products/{slug}.yml`
- 複製圖片至：`src/assets/images/product/{slug}/`
- 更新產品目錄 `src/_data/products.yml`


### 服務端點與原則

- 上傳服務預設在 `http://localhost:5011/`
- 啟動前先確認沒有重複實例；建議以虛擬環境啟動


### 環境需求

- Python 3.10+
- `OPENAI_API_KEY` 需設定於環境或 `.env`

`.env` 範例：

```env
OPENAI_API_KEY=sk-xxx
```


### 啟動方式

1) 以專屬腳本啟動（推薦，會在 `product-generator-v2` 建立獨立 venv）：

```bash
cd product-generator-v2
./start_server.sh
```

2) 或手動啟動（使用根目錄 venv）：

```bash
source .venv/bin/activate
pip install flask python-dotenv pyyaml openai
python product-generator-v2/server.py
```

啟動後前往：`http://localhost:5011/`


### 上傳使用流程（Web UI）

1) 準備 ZIP（結構如下）
2) 進入上傳頁，拖曳或選擇 ZIP
3) 送出後等待處理完成，成功會回傳產品頁 URL


### 產品包 ZIP 規格

- ZIP 根目錄需包含：
  - `product.md`: 產品資料（英文），格式見下方
  - `images/`: 相關圖片（任意副檔名，SVG/JPG/PNG 皆可）

```
your-product.zip
├── product.md
└── images/
    ├── main.jpg
    ├── product-1.png
    ├── product-2.png
    ├── compat-laptop.svg
    ├── charger.svg
    └── variant-1.jpg
```


### product.md 內容格式（重點）

- 基本資訊

```markdown
# Product Name

Category: gan_charger | loopenergy | powerbank | flash_disk
Catalog Image: main.jpg            # 可選，用於產品卡

## Description
... one or more paragraphs ...
```

- 主要圖片清單（用於產品頁輪播）

```markdown
## Images
- images/product-1.png
- images/product-2.png
```

- 特色與規格

```markdown
## Key Features
- Bullet 1
- Bullet 2

## Technical Specs
- Name: Value
- Weight: 120g
```

- 詳細特色（可含圖）

```markdown
## Detailed Features

### Title of Feature A
Description paragraphs...
Benefits:
- Benefit A1
- Benefit A2
Image: images/feature-a.png
Alt: Feature illustration

### Title of Feature B
...
```

- 相容性（圖示可選）

```markdown
## Compatibility
Title: Works with most USB-powered devices.
Subtitle: Laptops, tablets, phones, and accessories.
- Laptops
  Icon: images/compat-laptop.svg
- Tablets
  Icon: images/compat-tablet.svg
- Smartphones
  Icon: images/compat-phone.svg
- Accessories
  Icon: images/compat-accessory.svg
```

- 包裝內容（圖示可選）

```markdown
## Package Contents
Title: Everything you need in the box.
Subtitle: What's included
- Charger
  Icon: images/charger.svg
- Cable
  Icon: images/cable.svg
- Manual
```

- 其他包裝／型號（Also Available In）

```markdown
## Also Available In

### 2 Pack
Model Name: Loopenergy AAA Pro 2 Pack
SKU: AA-2P
EAN: 1234567890123
<!-- package_image: images/variant-2pack.jpg -->

### 4 Pack
Model Name: Loopenergy AAA Pro 4 Pack
SKU: AA-4P
EAN: 1234567890124
<!-- package_image: images/variant-4pack.jpg -->
```


### 產出規則與路徑對應

- 單品 YAML：`src/_data/products/{slug}.yml`，同時含 `en` 與 `de` 鍵
- 產品圖片：複製到 `src/assets/images/product/{slug}/`
- 首圖（catalog card）：
  - 優先 `Catalog Image` → `assets/images/product/{slug}/{file}`
  - 其次 `Images` 的第 1 張
  - 否則預設 `assets/images/product/{slug}/product-1.svg`
- 產品頁 URL：`/{lang}/products/{slugified-name}/`（以對應語系的 `name` slug 計算）
- 產品目錄更新：將卡片加入 `src/_data/products.yml` 對應分類


### 圖示（icon）規則

- 推薦統一放置於全域目錄：`assets/images/icons/`
- 在 product.md 內，`Icon:` 可填：
  - `icons/<file>.svg`（推薦，全站共用）
  - 或僅檔名（如 `charger.svg`，會被視為產品專屬圖示並放到 `assets/images/product/{slug}/`）
- 若未提供 icon，頁面會使用內建預設 SVG
- 聯絡頁（contact）另有內嵌鍵值對映（`phone|email|office`），與產品頁無關


### 常見錯誤

- SVG 解析錯誤：請確保 SVG 檔只有一個 `<svg>` 根元素
- 圖片遺失：確認 `product.md` 內路徑為 `images/xxx` 且 ZIP 內確實存在
- 404：若 `name` 更新會影響最終 permalink；V2 已將 catalog URL 與 Eleventy 一致化
- OPENAI_API_KEY 未設：解析或翻譯會失敗（伺服器日誌見 `product-generator-v2/server.log`）


### API（可選）

POST `http://localhost:5011/upload`

form-data: `file=@your-product.zip`

回應 200 範例：

```json
{ "message": "Product processed successfully!", "product_url": "/en/products/your-slug/" }
```


### 版本

- LLM 模型：`gpt-4.1-mini`
- 解析與翻譯透過 OpenAI Chat Completions（JSON 模式）


