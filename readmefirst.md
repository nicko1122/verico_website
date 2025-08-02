# ❗專案重要原則
你正參與一個 Verico 的企業網站重構專案，所有頁面必須轉換為：
- 11ty 無頭 CMS 架構
- 多語言支援（`en/`, `de/`）
- 使用 YAML 作為資料來源
- 嚴格模組化 nav/footer/head 等共用元件

# 📄 唯一資料規格來源
你必須完全遵循下列官方規格說明，不可自行解釋、創造或硬編碼資料。

== 開始規格 ==
詳見Verico專案開發說明.md
== 結束規格 ==

---

# ✅ 任務輸出格式標準

## ✅ 每個 `.njk` 頁面：
- 不得包含任何靜態字串或圖片（包括 hero 標語、產品名稱、分類標題）
- 所有內容必須來自對應 `_data/*.yml`
- 使用 `eleventyComputed.lang` 推斷語言（如 `/en/`, `/de/`）

## ✅ 共用模組：
| 元件        | 放置                 |
|-------------|----------------------|
| 導覽列      | `_includes/nav.njk`   |
| 頁尾        | `_includes/footer.njk`|
| head 區塊   | `_includes/head.njk`  |
| layout 框架 | `_includes/layout.njk`|

## ✅ YAML 規範
| 頁面            | YAML 檔案                     |
|-----------------|------------------------------|
| 首頁            | `_data/index.{lang}.yml`     |
| 產品分類總覽    | `_data/products.{lang}.yml`  |
| 單品詳細頁      | `_data/product-{slug}.{lang}.yml` |
| 聯絡頁/FAQ      | `_data/contact.{lang}.yml`   |
| 導覽列/nav menu | `_data/navigation.yml`       |
| 品牌設定        | `_data/site.yml`             |

---

# 🔍 驗收條件（完成後須回報）

- [ ] nav 與 footer 是否為共用 template？
- [ ] 所有資料是否來自 YAML？
- [ ] 是否支援多語資料抽換？
- [ ] 是否正確設定 `permalink` 與 `lang`？
- [ ] 是否避免任何硬編碼圖片與文案？

---
