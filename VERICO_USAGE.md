Verico 專案 使用說明書
=========================

1. 簡介
---------
本文件說明近期在專案中的變更、如何設定首頁 Hero 輪播、語系(i18n)設定、聯絡按鈕/表單的 mailto 行為，以及如何修改／新增翻譯字串。

2. 主要變更（概覽）
------------------
- Hero 輪播：將首頁 Hero 改為從 `src/assets/images/banner/hero/Carousel` 的圖片陣列做輪播（每張 slide 可在 YAML 設定 `image`, `slogan`, `position`）。
- Slogan 位置：支援九宮格位置設定（`LT, LC, LB, CT, CC, CB, RT, RC, RB`），模板會根據 `position` 產生對應的 Tailwind class。
- i18n：把多個原本硬編碼的文字搬到 `src/_data/i18n.yml`（包含 nav、redirect、catalog 三個 feature 區塊、product label 等）。
- Contact：產品頁與聯絡頁皆改為以 YAML 管理收件 email（`src/_data/i18n.yml` 中的 `buttons.contact_sales_email`），並以 `mailto:` 打開使用者郵件程式。聯絡表單會攔截 submit 並組成 mailto 連結。

3. 主要檔案與欄位說明
---------------------
- Hero / 輪播
  - `src/_data/homepage.yml`:
    - `hero.slides[]` 每項包含：
      - `image`: 圖片路徑（相對於站點根目錄，例如 `assets/images/...`）
      - `slogan`: 要顯示的標語（可包含 `<br>`，模板會使用 `| safe`）
      - `position`: 顯示位置（例如 `RC`，預設 `RC`）
  - 模板：`src/en/index.njk` / `src/de/index.njk` 會依 `slides` 迴圈渲染並套用位置 class

- i18n
  - `src/_data/i18n.yml`:
    - `en`, `de` 下包含語系字串，例如：
      - `nav.language_en`, `nav.language_de`
      - `global.redirect.title` / `sr_only` / `noscript_*`
      - `catalog.*`（why_title, why_text, quality_title/text, ...）
      - `product.label.model_name` / `sku` / `ean`
      - `buttons.contact_sales_email`（產品頁及聯絡表單會讀取此值）

- Contact
  - `src/en/contact.njk`, `src/de/contact.njk`：表單 submit 會用 JS 組成 `mailto:`，收件人由 `i18n[lang].buttons.contact_sales_email` 決定；主旨會包含表單標題與選擇的 subject。
  - `src/products.njk`：Contact Sales 按鈕已改為 `mailto:{{ i18n[product.lang].buttons.contact_sales_email }}?subject=Inquiry%20about%20<product>`

4. 如何新增 / 編輯 Hero Slides
-----------------------------
1. 把圖片放到 `src/assets/images/banner/hero/Carousel/`。
2. 編輯 `src/_data/homepage.yml`，在 `en.hero.slides` / `de.hero.slides` 新增一筆：
   - `image`: 圖片路徑
   - `slogan`: 標語
   - `position`: 位置代碼（可選，預設 `RC`）

範例：
```
- image: assets/images/banner/hero/Carousel/usb-banner.jpg
  slogan: "USB 傳輸快速又穩定"
  position: LB
```

5. 如何修改語系字串（i18n）
---------------------------
1. 開啟 `src/_data/i18n.yml`，找到對應語系（`en` 或 `de`）。
2. 修改現有 key 或新增 key，然後在模板中以 `{{ i18n[lang].path.to.key }}` 取用。

6. Contact mailto 行為說明
-------------------------
- 產品頁按鈕：會直接開啟 mailto，預設主旨 `Inquiry about <product name>`。
- 聯絡表單：按 Submit 後，前端 JS 會組出包含 Name/Email/Company/Subject/Message 的郵件內文，並使用 `mailto:` 打開郵件客戶端。若要改為 server-side 發信，需新增後端 API 來處理表單。

7. 開發與部署
----------------
- 本地開發（專案使用 Eleventy）請依專案 README 運行 local server（例如 `npm install` / `npm run dev`，若有不同請參考專案內說明）。

8. Git commit / push
--------------------
- 我已在本次變更中新增並提交本說明文件，commit 訊息：
  "i18n: move hardcoded strings to YAML; hero carousel & slogan position; contact mailto; add usage doc"

9. 若要我繼續做的項目
----------------------
- 自動把 `src/assets/images/banner/hero/Carousel` 的所有圖片加入 `homepage.yml`（並為每張建立空 slogan/預設位置）
- 把 `i18n.yml` 拆成多個語系檔 (`src/_data/i18n/en.yml`, `src/_data/i18n/de.yml`)
- 把聯絡表單改為 server-side 發信（需要後端或第三方服務）

如需我繼續執行以上任一項目或調整文案格式，請回覆告訴我要做哪一項。


