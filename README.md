### Verico Website (11ty Headless CMS)

本專案將既有靜態網站轉為以 Eleventy (11ty) 為核心的可維護、多語系 Headless CMS。內容資料以 YAML 驅動、模板採 Nunjucks、樣式使用 Tailwind（CDN 版本），並以自動化工具 Product-Generator-V2 產出產品頁面所需的 YAML 與圖片資產。

- **主要技術**: 11ty、Nunjucks、YAML、Tailwind (CDN)、Node.js、Python、Flask
- **多語系**: 英文 `en`、德文 `de`
- **自動化**: `product-generator-v2` 讀取 ZIP（含 `product.md` 與 `images/`），解析與翻譯後輸出 `src/_data/products/{slug}.yml` 和產品圖檔


### 目錄結構（精簡）

```text
src/
  _data/
    i18n.yml              # 多語 label/title 字串
    navigation.yml        # 多語導覽列
    products.yml          # 產品目錄（catalog）資料（由 V2 產生器更新）
    products/*.yml        # 單一產品資料（由 V2 產生器產出）
  _includes/
    layout.njk
    head.njk
    nav.njk
    footer.njk
  en/*.njk                # 英文頁面
  de/*.njk                # 德文頁面
  assets/
    images/
      product/{slug}/*    # 產品圖片（由 V2 產生器拷貝）
    css/style.css
.eleventy.js
product-generator-v2/
  server.py               # Flask 上傳服務
  start_server.sh         # 快速啟動腳本（會在此資料夾建立獨立 venv）
  processor_v2.py         # ZIP 解析/翻譯/輸出邏輯
  templates/index.html    # 上傳 UI
```


### 安裝需求

- Node.js 18+（建議 18 LTS 以上）
- Python 3.10+、pip、venv
- Git


### 服務啟動與關閉原則

- 請先確認同一服務沒有在背景執行，再啟動新的實例。
- 建議在專案根目錄啟用 Python venv 再啟動 Python 服務（若改以子資料夾的 `start_server.sh`，會在該資料夾自行建立 venv）。


### 專案初始化

1) 安裝 Node 相依

```bash
npm install
```

2)（可選）建立根目錄 Python 虛擬環境（供手動啟動 product-generator-v2 使用）

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install flask python-dotenv pyyaml openai
```


### 開發模式（11ty）

- 啟動 11ty Dev Server：

```bash
npm start
```

- 開啟瀏覽器：`http://localhost:8080/`
- 本站根頁會跳轉至 `/en/`；語系切換請用右上角選單。


### 建置（Build）

```bash
npm run build
```

結果輸出至 `_site/`。


### 多語與資料來源

- 全域資料：`src/_data/*.yml`
- 產品目錄：`src/_data/products.yml`（由產生器更新，含各語系類別/分頁 tabs 與產品卡）
- 單頁產品：`src/_data/products/{slug}.yml`（含 `en`、`de` 區塊；由產生器輸出）
- 模板：`src/_includes/*.njk`，頁面檔 `src/{lang}/*.njk`
- 產品頁模板：`src/products.njk` 使用 Eleventy `collections.allProducts` 分頁，`permalink` 由 `product[lang].name | slug` 計算


### 新增/更新產品資料（建議用 Product-Generator-V2）

請見操作手冊 `docs/Product-Generator-V2.md`：

- 使用 ZIP（根目錄 `product.md` + `images/`）上傳
- 自動解析英文結構、翻譯德文、產生 YAML、複製圖片、更新 `products.yml`

Icons（全站共用）
- 共用資料夾：`src/assets/images/icons/`
- 在 `product.md` 以 `Icon: icons/<file>.svg` 使用（不要加開頭斜線）
- 若使用僅檔名（如 `Icon: cable.svg`），會視為產品專屬圖示，路徑為 `assets/images/product/{slug}/cable.svg`


### 常見問題（節錄）

- 首頁空白/`homepage` 讀取不到：`.eleventy.js` 已加入 `yml` Data Extension；若自訂資料檔命名或路徑，需確保在 `_data/` 下且為有效 YAML。
- 圖片路徑錯誤：模板皆使用 `{{ ('/' + path) | url }}`，請確認資料中的路徑相對於專案根，例如 `assets/images/product/{slug}/file.png`。
- Product 404：產品卡/導覽連結會導至 `/en|de/products/{slugified-name}/`，若資料中名稱與實際頁面 `name` 不一致，URL 可能對不上；V2 產生器已將 catalog URL 與 Eleventy 規則對齊。
- OpenAI 金鑰：未設定 `OPENAI_API_KEY` 會導致解析/翻譯失敗。


### 授權

本專案原始碼依照倉庫 `LICENSE`（若存在）之條款釋出。品牌、圖片與商品資訊之著作權屬原權利人所有。


