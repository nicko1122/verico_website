# Verico 網站操作手冊(OPERATIONS)

> **忘記怎麼操作時,看這一份就夠。**
> 最後更新:2026-07-14 · 適用版本:main(`944fd9d` 之後)

---

## 0. 這個 Repo 是怎麼運作的(全貌)

```
┌────────────────────────────────────────────────────────────┐
│ ① 內容產生(Python 後台工具,只在本機跑,不部署)            │
│    產品 ZIP(product.md + images/)                          │
│      └─► product-manager(:5012)/ generator-v2(:5011)      │
│            └─► LLM 解析英文 + 翻譯德文                       │
│                  └─► src/_data/products/{slug}.yml           │
│                      src/assets/images/product/{slug}/       │
│                      更新 src/_data/products.yml(目錄卡片)  │
├────────────────────────────────────────────────────────────┤
│ ② 網站建置(11ty)                                           │
│    YAML 資料 + Nunjucks 模板 ──► npm run build ──► _site/    │
├────────────────────────────────────────────────────────────┤
│ ③ 部署(shell 腳本)                                         │
│    _site/ ──► FTP ──► ftp.vericoglobal.com(正式站)          │
└────────────────────────────────────────────────────────────┘
```

- **多語系**:英文 `en` + 德文 `de`,同一份 YAML 內分 `en:` / `de:` 區塊
- **唯一真實來源**:GitHub `nicko1122/verico_website`(main)
- **原始素材庫**(不在 repo 內):`D:\Desktop\verico-web-2025\`,其中 `product-package-md/` 是產品 ZIP 的文件結構參考

---

## 1. 新機器初始化

需求:**Node.js 18+**、**Python 3.10+**、git;部署另需 `lftp`、`curl`。

```bash
git clone git@github.com:nicko1122/verico_website.git verico
cd verico
npm install
```

環境設定(LLM 金鑰 + FTP 部署帳密,單一 `.env` 管理):

```bash
cp .env.example .env
# 然後編輯 .env 填入 OPENAI_API_KEY 與 FTP_HOST / FTP_USER / FTP_PASS
```

`.env` 已被 `.gitignore` 排除,不會進版控。

---

## 2. 日常操作速查表

| 想做什麼 | 指令 | 結果 |
|----------|------|------|
| 本地預覽 | `npm start` | http://localhost:8080/ (自動 rebuild) |
| 建置 | `npm run build` | 輸出到 `_site/` |
| 清掉重建 | `npm run rebuild` | 清 `_site` 後重建 |
| 產品後台(上傳/列表/下架) | `cd product-manager && ./start_server.sh` | http://localhost:5012/ |
| 只要上傳產生器 | `cd product-generator-v2 && ./start_server.sh` | http://localhost:5011/ |
| **增量部署**(推薦) | `./upload_checksum_manifest.sh` | 比對 sha1 只傳差異;`--dry-run` 先看會傳什麼 |
| 全量部署 | `./upload_to_ftp.sh` | lftp 整包上傳 `_site/` |

**建議完整流程**:上傳產品 ZIP → `npm start` 本地確認 → `git add/commit/push` → `npm run build` → `./upload_checksum_manifest.sh`

> ⚠️ 產生器/後台會**直接改動 `src/`**(YAML+圖片),做完記得 commit + push,不然只存在那台機器上。

---

## 3. 產品管理

### 3.1 新增產品
1. 準備 ZIP(手工組裝,文件結構參考 `D:\Desktop\verico-web-2025\product-package-md\`;格式範例見 `ref_only/`、可測試的完整範例見 `Sample-data/loopenergy-aa2550.zip`):
   ```
   my-product.zip
   ├─ product.md      ← 英文產品資料(格式見 docs/Product-Generator-V2.md)
   └─ images/         ← 圖片(png/jpg/svg 皆可)
   ```
2. 起後台:`cd product-manager && ./start_server.sh` → 開 http://localhost:5012/
3. 上傳 ZIP → 自動解析、翻譯德文、產 YAML、複製圖片、更新目錄
4. 本地預覽確認 → commit → build → 部署

### 3.2 更新產品
**同名 ZIP 再上傳一次即覆寫**(以 ZIP 檔名對應 YAML 檔名)。

### 3.3 下架產品
後台(:5012)列表勾選 → 刪除。會移除 YAML、圖片資料夾、目錄卡片。
備份 ZIP 永遠留在 `product-manager/backups/`,要恢復就重新上傳。

### 3.4 Icon 規則(product.md 內)
- 共用 icon:`Icon: icons/<file>.svg`(存放於 `src/assets/images/icons/`,**開頭不要加斜線**)
- 產品專屬 icon:只寫檔名(如 `Icon: cable.svg`)→ 對應 `assets/images/product/{slug}/cable.svg`

詳細:`docs/Product-Generator-V2.md`(ZIP/product.md 完整規格)、`docs/Product-Manager.md`(後台 API)

---

## 4. 內容編輯速查(哪個 YAML 管哪個頁面)

| 要改什麼 | 編輯這個檔 | 用在哪 |
|----------|-----------|--------|
| 首頁 Hero 輪播、分類、熱門產品 | `src/_data/homepage.yml` | `src/en|de/index.njk` |
| 聯絡頁(表單/FAQ/公司資訊) | `src/_data/contact.yml` | `src/en|de/contact.njk` |
| 按鈕文案、產品頁 label、**收件 email** | `src/_data/i18n.yml` | 幾乎所有模板 |
| 導覽選單結構 | `src/_data/navigation.yml` | `src/_includes/nav.njk` |
| 產品目錄(分類/卡片) | `src/_data/products.yml` | `src/en|de/product-catalog.njk`(通常由產生器維護,勿手改順序格式) |
| 單一產品內容 | `src/_data/products/{slug}.yml` | `src/products.njk`(產品頁模板) |
| Logo 路徑、頁尾文字 | `src/_data/site.yml` | `nav.njk` / `footer.njk` |

模板取用方式:`{% set data = homepage[lang] %}` → `{{ data.hero.title }}`;共用字串 `{{ i18n[lang].buttons.contact_sales }}`。

---

## 5. 常見修改場景

### 5.1 首頁 Hero 輪播
1. 圖片放 `src/assets/images/banner/hero/Carousel/`
2. 編輯 `src/_data/homepage.yml` 的 `en.hero.slides` / `de.hero.slides`:
   ```yaml
   - image: assets/images/banner/hero/Carousel/usb-banner.jpg
     slogan: "USB 傳輸快速又穩定"   # 可含 <br>
     position: LB                    # 九宮格:LT LC LB / CT CC CB / RT RC RB,預設 RC
   ```

### 5.2 改收件 Email(Contact Sales / 聯絡表單)
`src/_data/i18n.yml` → `en.buttons.contact_sales_email` / `de.buttons.contact_sales_email`。
表單與產品頁按鈕都是 **mailto:** 行為(前端組信,無後端寄信)。

### 5.3 改語系字串
`src/_data/i18n.yml` 對應語系底下改 key;模板以 `{{ i18n[lang].path.to.key }}` 取用。

---

## 6. 部署細節

- 目標主機與帳密:設定於 repo 根目錄 `.env`(`FTP_HOST` / `FTP_USER` / `FTP_PASS`,範本見 `.env.example`);未設定時腳本會直接報錯提示
- 選填參數:`FTP_REMOTE_DIR`(遠端根目錄,預設 `/`)、`UPLOAD_PARALLEL`(增量上傳並行數,預設 8,CLI `--parallel N` 可覆寫)
- 部署前**必須先 `npm run build`**(腳本只搬 `_site/`,不會幫你 build)
- `upload_checksum_manifest.sh`:本地算 sha1 清單 → 下載遠端 `.site_manifest.json` 比對 → 只傳差異(curl 並行,`--parallel N` 可調)→ 更新遠端 manifest
- 第一次或懷疑遠端狀態不對時,用 `./upload_to_ftp.sh` 全量傳一次

---

## 7. 疑難排解

| 症狀 | 原因/解法 |
|------|----------|
| 直接開 `_site/*.html` 圖片全破 | 正常。站內資源都是絕對路徑 `/assets/...`,要用 `npm start` 經 server 看 |
| 首頁空白 / 資料讀不到 | `_data/` 下 YAML 格式錯誤;`.eleventy.js` 已支援 `.yml`,檢查該檔可否被 yaml.load |
| 產品頁 404 | URL 由**英文名稱 slug** 產生,資料裡 name 改了 URL 就變;產生器已對齊規則,手改 name 要留意 |
| 產生器解析/翻譯失敗 | `OPENAI_API_KEY` 沒設(`.env` 或環境變數) |
| build 後樣式異常 | 樣式=Tailwind CDN + `src/assets/css/style.css`;檢查 `_site/assets/css/style.css` 是否存在 |
| commit 出現大量衝突標記 | 看到「解決合併衝突」類 commit 先驗內容再信(2025-10 曾發生壞合併把 CSS 刪掉,教訓) |

---

## 8. 文件地圖

| 文件 | 內容 |
|------|------|
| `README.md` | 專案概觀 + 快速開始 |
| `docs/OPERATIONS.md` | **本文件**,日常操作總入口 |
| `docs/Product-Generator-V2.md` | ZIP / product.md 完整格式規格 |
| `docs/Product-Manager.md` | 後台功能與 API |
| `docs/product-list.md` | 全產品規劃清單(含未上站產品) |
| `docs/archive/` | 歷史開發筆記(僅供考古) |
| `ref_only/` | product.md 各種寫法範例(含 HTML 標記圖片) |
| `Sample-data/` | 可直接測試上傳的範例 ZIP |
| `product-text/` | 產品原始文案素材 |
