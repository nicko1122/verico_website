# Verico Website

Verico 產品官網(行動電源、GaN 充電器、SSD、電池等),以 **Eleventy (11ty)** 為核心的靜態網站 + 輕量 Headless CMS:內容用 YAML 驅動、模板用 Nunjucks、樣式用 Tailwind(CDN),並附 Python 後台工具自動化產品資料的產生與管理。

- **技術**:11ty 3.x · Nunjucks · YAML · Tailwind (CDN) · Node.js 18+ · Python 3.10+ (Flask)
- **多語系**:英文 `en` / 德文 `de`(單一 YAML 內分區塊)
- **正式站**:vericoglobal.com(FTP 部署)

> 📖 **日常操作(預覽/建置/加產品/部署)請看 [`docs/OPERATIONS.md`](docs/OPERATIONS.md) —— 忘記怎麼用時從那裡開始。**

## 快速開始

```bash
npm install
npm start        # 開發模式 → http://localhost:8080/(根頁自動跳轉 /en/)
npm run build    # 建置 → _site/
```

產品後台(上傳 ZIP 自動產生產品頁,需 `OPENAI_API_KEY` 於 `.env`):

```bash
cd product-manager && ./start_server.sh   # → http://localhost:5012/
```

## 目錄結構(精簡)

```text
src/
  _data/
    i18n.yml              # 多語字串(按鈕/label/email)
    navigation.yml        # 導覽列
    homepage.yml          # 首頁(Hero 輪播等)
    contact.yml           # 聯絡頁
    products.yml          # 產品目錄(由產生器維護)
    products/{slug}.yml   # 單一產品資料(由產生器產出)
  _includes/              # layout / head / nav / footer 模板
  en/ de/                 # 各語系頁面
  products.njk            # 產品頁模板(pagination 自動產生所有產品頁)
  assets/                 # CSS 與全部圖片(css/style.css、images/...)
.eleventy.js              # 11ty 設定(collections、slug、cache-bust filter)
product-generator-v2/     # ZIP → YAML+圖片 產生器(:5011)
product-manager/          # 產品後台:上傳/列表/下架(:5012)
docs/                     # 操作手冊與工具文件
ref_only/  Sample-data/   # product.md 格式範例 / 測試 ZIP
upload_checksum_manifest.sh  upload_to_ftp.sh   # FTP 部署腳本
```

## 文件

| 我想… | 看這份 |
|--------|--------|
| 日常操作總覽(必讀) | [`docs/OPERATIONS.md`](docs/OPERATIONS.md) |
| 產品 ZIP / product.md 格式 | [`docs/Product-Generator-V2.md`](docs/Product-Generator-V2.md) |
| 後台功能與 API | [`docs/Product-Manager.md`](docs/Product-Manager.md) |
| 歷史開發筆記 | `docs/archive/` |

## 授權

原始碼依倉庫 LICENSE(若存在)條款釋出;品牌、圖片與商品資訊著作權屬原權利人所有。
