# 📋 Verico 專案轉換 Todo 清單

## 🎯 專案目標
將現有的 4 個靜態 HTML 頁面轉換為模組化、可維護的 11ty 無頭 CMS 架構，支援多語言功能。

### ⚠️ 重要提醒
- **務必與原"static"內的版型設計相符**
- **保持原有的視覺設計和用戶體驗**
- **確保所有靜態資源路徑正確**
- **維持原有的響應式設計效果**
---

## 📁 第一階段：專案初始化與配置

### ✅ 已完成
- [x] 靜態頁面開發完成（4 個 HTML 頁面）
- [x] Tailwind CSS 樣式實現
- [x] 響應式設計完成
- [x] 產品資料結構規劃

### 🔄 進行中
- [ ] 建立 11ty 專案結構
- [ ] 安裝必要依賴套件
- [ ] 配置 11ty 設定檔

### ⏳ 待完成
- [ ] 建立 `package.json`
- [ ] 安裝 11ty 和相關套件
- [ ] 建立 `.eleventy.js` 配置檔
- [ ] 設定 Tailwind CSS 編譯流程
- [ ] 建立開發和建置腳本
- [ ] 複製 static 資源到 src/assets
- [ ] 設定 CDN Tailwind CSS（主要使用）
- [ ] 配置自定義 CSS 選項（如需要）

---

## 🏗️ 第二階段：建立專案結構

### 📂 目錄結構建立
- [ ] 建立 `src/` 目錄
- [ ] 建立 `src/en/` 英文內容目錄
- [ ] 建立 `src/de/` 德文內容目錄
- [ ] 建立 `src/_data/` 資料目錄
- [ ] 建立 `src/_includes/` 模板目錄
- [ ] 建立 `src/assets/` 資源目錄
- [ ] 建立 `src/assets/css/` CSS 目錄
- [ ] 建立 `src/assets/js/` JavaScript 目錄
- [ ] 建立 `src/assets/images/` 圖片目錄（複製 static 資源）

### 📄 基礎模板建立
- [ ] 建立 `src/_includes/layout.njk` 主框架模板（包含頁框、head、nav、footer）
- [ ] 建立 `src/_includes/head.njk` 共用 head 模板（meta、fonts、css）
- [ ] 建立 `src/_includes/nav.njk` 導航模板（含語言切換器、submenu 支援）
- [ ] 建立 `src/_includes/footer.njk` 頁尾模板（公司資訊與版權）
- [ ] 建立 `src/_includes/product-card.njk` 產品卡片模板（可選：商品卡元件片段）

### 🔧 11ty 配置
- [ ] 建立 `.eleventy.js` 配置檔
- [ ] 設定 `permalink: /{{ lang }}/products/` 多語言路由
- [ ] 配置 Tailwind CSS 編譯流程
- [ ] 設定 `tailwind.config.js` 獨立配置
- [ ] 建立 PostCSS 配置（如需要自定義 CSS）
- [ ] 設定 `i18n` 國際化資料夾結構
- [ ] 配置 Nunjucks 模板引擎

---

## 📊 第三階段：資料架構建立

### 🗂️ YAML 資料檔案
- [ ] 建立 `src/_data/site.yml` 網站基本資訊（logo、品牌標語）
- [ ] 建立 `src/_data/navigation.yml` 多語言導航（含 i18n title）
- [ ] 建立 `src/_data/index.en.yml` 英文首頁資料（Hero + 區塊）
- [ ] 建立 `src/_data/index.de.yml` 德文首頁資料（Hero + 區塊）
- [ ] 建立 `src/_data/products.en.yml` 英文產品資料（產品類別與簡略資料）
- [ ] 建立 `src/_data/products.de.yml` 德文產品資料（產品類別與簡略資料）
- [ ] 建立 `src/_data/contact.en.yml` 英文聯絡資料（聯繫方式、FAQ）
- [ ] 建立 `src/_data/contact.de.yml` 德文聯絡資料（聯繫方式、FAQ）

### 📋 產品詳細資料（單一產品）
- [ ] 建立 `src/_data/product-mojo-140w-gan-charger.en.yml`
- [ ] 建立 `src/_data/product-mojo-140w-gan-charger.de.yml`
- [ ] 建立其他產品的詳細資料檔案
- [ ] 確保產品資料包含：title、series、description、images、features、specs、compatibility、package
- [ ] 實現 `product-[slug].{lang}.yml` 命名規則
- [ ] 確保所有圖片路徑正確（assets/images/...）



---

## 🌐 第四階段：多語言頁面建立

### 🏠 首頁轉換
- [ ] 建立 `src/en/index.njk` 英文首頁
- [ ] 建立 `src/de/index.njk` 德文首頁
- [ ] 實現 Hero 區塊動態化（圖片、標語）
- [ ] 實現產品分類區塊動態化（Power Pro Series 等）
- [ ] 實現熱門產品區塊動態化（trending_products）
- [ ] 使用 `loop` 自動 render 產品網格

### 📦 產品目錄頁轉換
- [ ] 建立 `src/en/product-catalog.njk` 英文產品目錄
- [ ] 建立 `src/de/product-catalog.njk` 德文產品目錄
- [ ] 實現產品分類篩選功能
- [ ] 實現產品卡片動態渲染
- [ ] 實現產品類別與簡略資料展示

### 📄 產品詳細頁轉換
- [ ] 建立 `src/en/products/{slug}/index.njk` 英文產品詳細頁
- [ ] 建立 `src/de/products/{slug}/index.njk` 德文產品詳細頁
- [ ] 實現產品圖片輪播
- [ ] 實現產品規格動態渲染
- [ ] 實現產品特色區塊（features）
- [ ] 實現相容性清單（compatibility）
- [ ] 實現包裝內容清單（package）
- [ ] 實現單一產品詳細資料展示

### 📞 聯絡頁轉換
- [ ] 建立 `src/en/contact.njk` 英文聯絡頁
- [ ] 建立 `src/de/contact.njk` 德文聯絡頁
- [ ] 實現聯絡資訊動態化（電話、郵件、地址）
- [ ] 實現 FAQ 區塊動態化（問答與公司資訊資料分離）
- [ ] 實現聯絡表單功能

---

## 🎨 第五階段：樣式與互動功能

### 🎯 CSS 樣式
- [ ] 設定 Tailwind CSS 配置
- [ ] 建立 `tailwind.config.js` 獨立配置
- [ ] 建立自訂 CSS 檔案（`assets/css/main.css`）
- [ ] 實現玻璃擬態效果（backdrop-blur）
- [ ] 確保響應式設計
- [ ] 優化載入效能
- [ ] 配置 PostCSS（如需要自定義樣式）
- [ ] 主要以 CDN tailwind 為主
- [ ] 配置自定義樣式選項（可選）

### ⚡ JavaScript 功能
- [ ] 實現語言切換功能（dropdown + 路徑自動切換）
- [ ] 實現產品下拉選單（含 submenu 支援）
- [ ] 實現圖片輪播功能
- [ ] 實現表單驗證
- [ ] 實現平滑滾動效果
- [ ] 實現產品分類切換功能
- [ ] 模組化放入 `assets/js/*.js`
- [ ] 在 `layout.njk` 統一引入 JS 檔案
- [ ] 建立 `assets/js/lang-toggle.js` 語言切換腳本
- [ ] 實現常見功能：語言切換器、產品分類切換、下拉選單、圖片輪播

---

## 🔧 第六階段：功能測試與優化

### 🧪 功能測試
- [ ] 測試多語言切換功能（`/en/...` ↔ `/de/...`）
- [ ] 測試產品頁面路由（`permalink: /{{ lang }}/products/`）
- [ ] 測試響應式設計
- [ ] 測試表單提交功能
- [ ] 測試圖片載入效能
- [ ] 測試導航選單 submenu 功能
- [ ] 測試 `page.lang` 語系選擇功能
- [ ] 測試 `{% set t = nav.title[lang] or nav.title['en'] %}` 語系選擇
- [ ] 測試 `loop` 自動 render 功能
- [ ] 測試所有 YAML 資料檔案載入
- [ ] 測試所有圖片路徑正確性

### ⚡ 效能優化
- [ ] 圖片壓縮和優化
- [ ] CSS/JS 檔案壓縮
- [ ] 設定快取策略
- [ ] 優化載入速度
- [ ] SEO 優化

### 🔍 SEO 與 Meta 標籤
- [ ] 設定多語言 meta 標籤
- [ ] 建立 sitemap.xml
- [ ] 設定 robots.txt
- [ ] 實現 Open Graph 標籤
- [ ] 實現結構化資料

---

## 🚀 第七階段：部署與維護

### 📦 建置配置
- [ ] 設定生產環境建置
- [ ] 配置靜態檔案服務
- [ ] 設定 CDN 配置
- [ ] 建立部署腳本

### 📊 監控與維護
- [ ] 設定錯誤監控
- [ ] 建立備份策略
- [ ] 設定更新流程
- [ ] 建立文件說明

---

## 📋 檢查清單

### 🔄 每階段完成檢查
- [ ] 程式碼符合專案規範
- [ ] 多語言功能正常運作
- [ ] 響應式設計測試通過
- [ ] 效能指標達標
- [ ] SEO 最佳化完成
- [ ] 與原"static"版型設計相符
- [ ] 所有字串和圖片都從 YAML 資料讀取
- [ ] 模組化 partial 共用正常
- [ ] 模組化資源統一引入正常

### 🎯 最終驗收標準
- [ ] 所有靜態頁面成功轉換為 11ty 模板
- [ ] 多語言功能完整實現（英文、德文）
- [ ] 資料與模板完全分離（YAML 資料檔案）
- [ ] 網站效能優化完成
- [ ] 部署流程順暢
- [ ] 與原"static"版型設計完全相符
- [ ] 所有字串和圖片都從 YAML 資料讀取
- [ ] 多語言路由正確運作（`/en/...` ↔ `/de/...`）
- [ ] 所有元件功能正常：nav/footer、首頁 hero、Product grid、FAQ/聯絡
- [ ] 所有模板結構正常：模組化 partial 共用、模組化資源統一引入

---

## 📝 注意事項

### ⚠️ 重要提醒
1. **服務端點確認**：確保所有服務端點正常運作
2. **VENV 環境**：使用虛擬環境啟動服務
3. **架構不變**：未經明確指示不得更動架構
4. **英文程式碼**：所有程式碼必須使用英文
5. **中文回應**：所有回應使用中文
6. **版型一致性**：務必與原"static"內的版型設計相符
7. **多語言路由**：使用 `permalink: /{{ lang }}/products/` 控制輸出路徑
8. **資料分離**：所有字串和圖片不得寫死在模板內，必須使用 YAML 資料

### 🔄 開發流程
1. 先討論確認需求
2. 按階段逐步實現
3. 每階段完成後測試
4. 確保符合專案規範

---

## 📅 時間規劃

| 階段 | 預計時間 | 狀態 |
|------|----------|------|
| 第一階段：專案初始化 | 1-2 天 | ⏳ 待開始 |
| 第二階段：建立結構 | 2-3 天 | ⏳ 待開始 |
| 第三階段：資料架構 | 2-3 天 | ⏳ 待開始 |
| 第四階段：頁面轉換 | 5-7 天 | ⏳ 待開始 |
| 第五階段：樣式功能 | 3-4 天 | ⏳ 待開始 |
| 第六階段：測試優化 | 2-3 天 | ⏳ 待開始 |
| 第七階段：部署維護 | 1-2 天 | ⏳ 待開始 |

**總預計時間：16-24 天**

---

## 🎯 下一步行動

1. **立即開始**：第一階段專案初始化
2. **優先順序**：建立基礎架構 → 資料分離 → 頁面轉換 → 功能完善
3. **持續追蹤**：定期更新此 Todo 清單進度
4. **品質保證**：每階段完成後進行測試和驗收

---

*最後更新：2024年12月*
*專案負責人：開發團隊* 