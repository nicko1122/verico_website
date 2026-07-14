YAML -> Pages 使用對照
======================

此文件列出專案中主要的 `src/_data` YAML 檔案，與在 `src/` 範本中會使用到它們的頁面/檔案，方便你快速定位要修改的欄位。

- `src/_data/homepage.yml`
  - 用於：`src/en/index.njk`, `src/de/index.njk`
  - 內容重點：`hero.slides[]`（每張 slide 含 `image`, `slogan`, `position`）、`categories`, `trending`, `tagline`, `about`。

- `src/_data/contact.yml`
  - 用於：`src/en/contact.njk`, `src/de/contact.njk`
  - 內容重點：`hero`, `contact_methods`, `form`（fields/labels/options）、`map`, `company_info`, `faq`。

- `src/_data/i18n.yml`
  - 用於：多個 template（語系字串），例如 `src/_includes/nav.njk`, `src/index.njk`, `src/en/product-catalog.njk`, `src/de/product-catalog.njk`, `src/products.njk`, `src/en/contact.njk`, `src/de/contact.njk`。
  - 內容重點：按鈕文案、global redirect 文案、catalog 區塊文字、product label（Model Name / SKU / EAN）與 contact email 等。

- `src/_data/navigation.yml`
  - 用於：`src/_includes/nav.njk`
  - 內容重點：網站主要選單結構（`main`）、submenu 與連結。

- `src/_data/products.yml` and `src/_data/products/*.yml`
  - 用於：`src/en/product-catalog.njk`, `src/de/product-catalog.njk`, `src/products.njk`（individual product pages come from `collections.allProducts` which are generated from these product YAMLs）
  - 內容重點：產品目錄、各產品條目（name/description/image/url）與 product-specific 資料檔（`src/_data/products/<product>.yml`）

- `src/_data/site.yml`
  - 用於：`src/_includes/footer.njk`, `src/_includes/nav.njk`（logo path / footer text 等）

快速定位說明
----------------
- 若要改首頁輪播，編輯 `src/_data/homepage.yml` 的 `en.hero.slides` / `de.hero.slides`。
- 若要改聯絡頁表單 label 或 FAQ，編輯 `src/_data/contact.yml` 對應欄位。
- 若要改一般文字（按鈕、catalog 標題、redirect 文案等），編輯 `src/_data/i18n.yml`。
- 若要改選單結構或連結，編輯 `src/_data/navigation.yml`。
- 若要改單一產品內容，編輯或新增 `src/_data/products/<product>.yml`（產品資料檔）或 `src/_data/products.yml` 中的列表。

如何在模板中使用
-------------------
- 基本存取方式：`{{ data.someKey }}` 或 `{{ i18n[lang].path.to.key }}`（視範本中設定的變數而定）。
- 範例：在 `src/en/index.njk` 中，首頁 hero 圖為 `data.hero.image`，當 `data = homepage.en`。

如果要，我可以：
- 將 `i18n.yml` 拆成 `src/_data/i18n/en.yml` / `de.yml`（便於維護）；或
- 自動把 `src/assets/images/banner/hero/Carousel` 的圖片加入 `homepage.yml`（建立 slides 條目）。

若需把此清單擴充到更多 YAML（或把每個 YAML 的所有 key 都輸出為文件），告訴我我要自動化的深度。


