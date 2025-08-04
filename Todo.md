# 📋 Verico 專案轉換 Todo 清單

## 🎯 專案目標
將現有的 4 個靜態 HTML 頁面轉換為模組化、可維護的 11ty 無頭 CMS 架構，支援多語言功能。

### ⚠️ 重要提醒
- **務必與原"static"內的版型設計相符**
- **保持原有的視覺設計和用戶體驗**
- **確保所有靜態資源路徑正確**
- **維持原有的響應式設計效果**
---

## 📁 第一階段：專案初始化與配置 ✅ 已完成

### ✅ 已完成
- [x] 靜態頁面開發完成（4 個 HTML 頁面）
- [x] Tailwind CSS 樣式實現
- [x] 響應式設計完成
- [x] 產品資料結構規劃
- [x] 建立 11ty 專案結構
- [x] 安裝必要依賴套件
- [x] 配置 11ty 設定檔
- [x] 建立 `package.json`
- [x] 安裝 11ty 和相關套件
- [x] 建立 `.eleventy.js` 配置檔
- [x] 設定 Tailwind CSS 編譯流程
- [x] 建立開發和建置腳本
- [x] 複製 static 資源到 src/assets
- [x] 設定 CDN Tailwind CSS（主要使用）
- [x] 配置自定義 CSS 選項（如需要）

---

## 🏗️ 第二階段：建立專案結構 ✅ 已完成

### ✅ 已完成
- [x] 建立 `src/` 目錄
- [x] 建立 `src/en/` 英文內容目錄
- [x] 建立 `src/de/` 德文內容目錄
- [x] 建立 `src/_data/` 資料目錄
- [x] 建立 `src/_includes/` 模板目錄
- [x] 建立 `src/assets/` 資源目錄
- [x] 建立 `src/assets/css/` CSS 目錄
- [x] 建立 `src/assets/js/` JavaScript 目錄
- [x] 建立 `src/assets/images/` 圖片目錄（複製 static 資源）
- [x] 建立 `src/_includes/layout.njk` 主框架模板（包含頁框、head、nav、footer）
- [x] 建立 `src/_includes/head.njk` 共用 head 模板（meta、fonts、css）
- [x] 建立 `src/_includes/nav.njk` 導航模板（含語言切換器、submenu 支援）
- [x] 建立 `src/_includes/footer.njk` 頁尾模板（公司資訊與版權）
- [x] 建立 `.eleventy.js` 配置檔
- [x] 設定 `permalink: /{{ lang }}/products/` 多語言路由
- [x] 配置 Tailwind CSS 編譯流程
- [x] 設定 `tailwind.config.js` 獨立配置
- [x] 建立 PostCSS 配置（如需要自定義 CSS）
- [x] 設定 `i18n` 國際化資料夾結構
- [x] 配置 Nunjucks 模板引擎

---

## 📊 第三階段：資料架構建立 ✅ 已完成

### ✅ 已完成
- [x] 建立 `src/_data/site/config.yml` 網站基本資訊（logo、品牌標語）
- [x] 建立 `src/_data/site/navigation.yml` 多語言導航（含 i18n title）
- [x] 建立 `src/_data/content/homepage/en.yml` 英文首頁資料（Hero + 區塊）
- [x] 建立 `src/_data/content/homepage/de.yml` 德文首頁資料（Hero + 區塊）
- [x] 建立 `src/_data/content/products/catalog/en.yml` 英文產品資料（產品類別與簡略資料）
- [x] 建立 `src/_data/content/products/catalog/de.yml` 德文產品資料（產品類別與簡略資料）
- [x] 建立 `src/_data/content/contact/en.yml` 英文聯絡資料（聯繫方式、FAQ）
- [x] 建立 `src/_data/content/contact/de.yml` 德文聯絡資料（聯繫方式、FAQ）
- [x] 實現多語言 Logo 動態切換功能
- [x] 修正圖片路徑問題（確保所有路徑以 `/` 開頭）
- [x] **多語言導航 URL 結構**：實現 `url: { en: /en/, de: /de/ }` 格式
- [x] **條件顯示功能**：實現 `available_in: [en]` 或 `available_in: [en, de]` 控制顯示

### 🔄 進行中
- [ ] 建立產品詳細資料檔案結構
- [ ] 實現 `product-[slug].{lang}.yml` 命名規則

---

## 🌐 第四階段：多語言頁面建立 🔄 進行中

### ✅ 已完成
- [x] 建立 `src/en/index.njk` 英文首頁
- [x] 建立 `src/de/index.njk` 德文首頁
- [x] 實現 Hero 區塊動態化（圖片、標語）
- [x] 實現產品分類區塊動態化（Power Pro Series 等）
- [x] 實現熱門產品區塊動態化（trending_products）
- [x] 使用 `loop` 自動 render 產品網格
- [x] 建立 `src/en/product-catalog.njk` 英文產品目錄
- [x] 建立 `src/de/product-catalog.njk` 德文產品目錄
- [x] 建立 `src/en/contact.njk` 英文聯絡頁
- [x] 建立 `src/de/contact.njk` 德文聯絡頁
- [x] 實現聯絡資訊動態化（電話、郵件、地址）
- [x] 實現 FAQ 區塊動態化（問答與公司資訊資料分離）
- [x] 建立 `src/en/products/gan-charger/index.njk` 英文產品詳細頁
- [x] 建立 `src/de/products/gan-charger/index.njk` 德文產品詳細頁
- [x] **完成首頁功能**：移除測試警告，添加完整樣式，確保與 static/index.html 完全一致
- [x] **修正 NAV 語言切換**：移除重複選單，使用與 static/index.html 相同的 select 語言選單
- [x] **修正跳轉頁面**：簡化為白色背景 + Verico Logo + Loading 文字，移除 nav 和 footer
- [x] **多語言導航功能**：實現多語言 URL 和條件顯示，支援不同語言版本顯示不同產品

### 🔄 進行中
- [ ] 實現產品分類篩選功能
- [ ] 實現產品卡片動態渲染
- [ ] 實現產品類別與簡略資料展示
- [ ] 實現產品圖片輪播
- [ ] 實現產品規格動態渲染
- [ ] 實現產品特色區塊（features）
- [ ] 實現相容性清單（compatibility）
- [ ] 實現包裝內容清單（package）
- [ ] 實現單一產品詳細資料展示
- [ ] 實現聯絡表單功能

### ⏳ 待完成
- [ ] 建立其他產品詳細頁面（powerbank、loopenergy、flash-disk 等）
- [ ] 完善所有產品頁面的功能

---

## 🎨 第五階段：樣式與互動功能 🔄 進行中

### ✅ 已完成
- [x] 設定 Tailwind CSS 配置
- [x] 建立 `tailwind.config.js` 獨立配置
- [x] 建立自訂 CSS 檔案（`assets/css/main.css`）
- [x] 實現玻璃擬態效果（backdrop-blur）
- [x] 確保響應式設計
- [x] 主要以 CDN tailwind 為主
- [x] 配置自定義樣式選項（可選）
- [x] 實現語言切換功能（dropdown + 路徑自動切換）
- [x] 實現產品下拉選單（含 submenu 支援）
- [x] 模組化放入 `assets/js/*.js`
- [x] 在 `layout.njk` 統一引入 JS 檔案
- [x] 建立 `assets/js/lang-toggle.js` 語言切換腳本
- [x] **修正 JavaScript 路徑**：所有 JS 路徑以 `/` 開頭
- [x] **完善語言切換功能**：桌面版和移動版 select 語言選單正常工作
- [x] **多語言導航模板**：nav.njk 支援多語言 URL 和條件顯示

### 🔄 進行中
- [ ] 實現圖片輪播功能
- [ ] 實現表單驗證
- [ ] 實現平滑滾動效果
- [ ] 實現產品分類切換功能
- [ ] 實現常見功能：語言切換器、產品分類切換、下拉選單、圖片輪播

---

## 🔧 第六階段：功能測試與優化 ⏳ 待開始

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
- [x] **測試多語言導航功能**：驗證不同語言版本顯示不同產品

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

## 🚀 第七階段：部署與維護 ⏳ 待開始

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

## 🎯 當前重點任務

### 🔥 優先級 1：完善核心功能
1. **完善產品詳細頁面**
   - [ ] 完善 gan-charger 產品頁面功能
   - [ ] 實現產品圖片輪播
   - [ ] 實現產品規格動態渲染
   - [ ] 實現產品特色區塊
   - [ ] 建立其他產品詳細頁面（powerbank、loopenergy、flash-disk）

2. **完善互動功能**
   - [ ] 實現圖片輪播功能
   - [ ] 實現表單驗證
   - [ ] 實現平滑滾動效果
   - [ ] 實現產品分類切換功能

3. **完善數據結構**
   - [ ] 建立產品詳細資料檔案
   - [ ] 實現 `product-[slug].{lang}.yml` 命名規則
   - [ ] 確保所有產品資料完整

### 🔥 優先級 2：優化與測試
1. **功能測試**
   - [ ] 測試多語言切換功能
   - [ ] 測試響應式設計
   - [ ] 測試圖片載入效能
   - [ ] 測試所有互動功能

2. **SEO 優化**
   - [ ] 設定多語言 meta 標籤
   - [ ] 建立 sitemap.xml
   - [ ] 實現 Open Graph 標籤

---

## 📋 檢查清單

### 🔄 每階段完成檢查
- [x] 程式碼符合專案規範
- [x] 多語言功能正常運作
- [x] 響應式設計測試通過
- [x] 與原"static"版型設計相符
- [x] 所有字串和圖片都從 YAML 資料讀取
- [x] 模組化 partial 共用正常
- [x] 模組化資源統一引入正常
- [ ] 效能指標達標
- [ ] SEO 最佳化完成

### 🎯 最終驗收標準
- [x] 所有靜態頁面成功轉換為 11ty 模板
- [x] 多語言功能完整實現（英文、德文）
- [x] 資料與模板完全分離（YAML 資料檔案）
- [x] 與原"static"版型設計完全相符
- [x] 所有字串和圖片都從 YAML 資料讀取
- [x] 多語言路由正確運作（`/en/...` ↔ `/de/...`）
- [x] 所有元件功能正常：nav/footer、首頁 hero、Product grid、FAQ/聯絡
- [x] 所有模板結構正常：模組化 partial 共用、模組化資源統一引入
- [x] **多語言導航功能**：支援不同語言版本顯示不同產品
- [ ] 網站效能優化完成
- [ ] 部署流程順暢

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
9. **圖片路徑規範**：所有圖片路徑必須以 `/` 開頭，確保正確顯示
10. **圖片存放位置**：所有新圖片都放在 `static/assets/images/` 目錄
11. **多語言導航**：使用 `available_in` 屬性控制產品在不同語言版本的顯示

### 🔄 開發流程
1. 先討論確認需求
2. 按階段逐步實現
3. 每階段完成後測試
4. 確保符合專案規範

---

## 📅 時間規劃

| 階段 | 預計時間 | 狀態 |
|------|----------|------|
| 第一階段：專案初始化 | 1-2 天 | ✅ 已完成 |
| 第二階段：建立結構 | 2-3 天 | ✅ 已完成 |
| 第三階段：資料架構 | 2-3 天 | ✅ 已完成 |
| 第四階段：頁面轉換 | 5-7 天 | 🔄 進行中 |
| 第五階段：樣式功能 | 3-4 天 | 🔄 進行中 |
| 第六階段：測試優化 | 2-3 天 | ⏳ 待開始 |
| 第七階段：部署維護 | 1-2 天 | ⏳ 待開始 |

**總預計時間：16-24 天**
**已完成時間：約 12-14 天**
**剩餘時間：約 4-10 天**

---

## 🎯 下一步行動

1. **立即開始**：完善產品詳細頁面功能
2. **優先順序**：產品詳細頁 → 互動功能 → 測試優化 → 部署
3. **持續追蹤**：定期更新此 Todo 清單進度
4. **品質保證**：每階段完成後進行測試和驗收

---

## 🏆 最新成就

### ✅ 已完成的重要功能
- [x] **多語言 Logo 動態切換**：英文使用 `verico-logo.svg`，德文使用 `perks_logo_s.png`
- [x] **圖片路徑問題解決**：所有圖片路徑都以 `/` 開頭，確保正確顯示
- [x] **數據結構重構**：將 `_data` 目錄重構為更有組織性的結構
- [x] **智能跳轉頁面**：實現根據用戶地區自動跳轉到相應語言版本
- [x] **語言切換器**：右上角語言切換器，支援手動語言切換
- [x] **Cookie 記憶功能**：記住用戶語言偏好，30天過期
- [x] **基礎頁面架構**：首頁、產品目錄、聯絡頁、產品詳細頁（gan-charger）
- [x] **首頁功能完善**：移除測試警告，添加完整樣式，確保與 static/index.html 完全一致
- [x] **NAV 語言切換修正**：移除重複選單，使用與 static/index.html 相同的 select 語言選單
- [x] **跳轉頁面簡化**：白色背景 + Verico Logo + Loading 文字，移除 nav 和 footer
- [x] **JavaScript 路徑修正**：所有 JS 路徑以 `/` 開頭，語言切換功能正常工作
- [x] **多語言導航功能**：實現多語言 URL 結構和條件顯示，支援不同語言版本顯示不同產品

### 🔄 當前進行中的工作
- [ ] 完善 gan-charger 產品詳細頁面功能
- [ ] 建立其他產品詳細頁面（powerbank、loopenergy、flash-disk）
- [ ] 實現圖片輪播等互動功能
- [ ] 完善表單驗證功能

---

## 🎯 多語言導航功能詳情

### ✅ 實現的功能
1. **多語言 URL 結構**
   ```yaml
   url:
     en: /en/products/powerbank/power-pro-20000mah
     de: /de/products/powerbank/power-pro-20000mah
   ```

2. **條件顯示控制**
   ```yaml
   available_in: [en]  # 只有英文版顯示
   available_in: [en, de]  # 兩種語言都顯示
   ```

3. **模板支援**
   - ✅ 桌面版導航支援多語言 URL
   - ✅ 移動版導航支援多語言 URL
   - ✅ 條件顯示：根據 `available_in` 屬性控制顯示

### 🎯 使用方式
- **添加新產品（兩種語言都有）**：設置 `available_in: [en, de]`
- **添加新產品（只有英文版）**：設置 `available_in: [en]`
- **添加新產品（只有德文版）**：設置 `available_in: [de]`

---

*最後更新：2024年12月*
*專案負責人：開發團隊* 