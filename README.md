# Verico 公司網站

這是一個使用 Eleventy (11ty) 構建的現代化公司網站，專注於電池與記憶體解決方案。

## 🚀 功能特色

- **⚡ 快速建置** - 使用 Eleventy 靜態網站生成器，載入速度快
- **📱 響應式設計** - 完美適配桌面和移動設備
- **🎨 現代化設計** - 玻璃態效果 (Glassmorphism) 設計風格
- **🔧 易於維護** - 模組化的代碼結構和數據驅動的內容管理
- **🌱 環保理念** - "ECO not EGO" 的永續發展理念
- **🔄 熱重載** - 開發時自動重新載入，提升開發效率

## 🏗️ 專案結構

```
verico/
├── src/
│   ├── _data/
│   │   ├── site.json              # 網站配置和內容
│   │   └── products.json          # 產品數據庫
│   ├── _includes/
│   │   ├── base.njk              # 基礎模板
│   │   ├── page.njk              # 頁面模板
│   │   └── product-spec.njk      # 產品規格模板
│   ├── assets/
│   │   ├── css/
│   │   │   ├── style.css         # 編譯後的樣式
│   │   │   └── tailwind.css      # Tailwind 入口文件
│   │   ├── js/
│   │   │   └── main.js           # JavaScript 功能
│   │   └── images/               # 圖片資源
│   ├── pages/                    # 靜態頁面
│   │   └── products/             # 產品頁面
│   └── index.njk                 # 首頁
├── static/                       # 靜態文件服務
├── _site/                        # 建置輸出目錄
├── .eleventy.js                  # Eleventy 配置
├── tailwind.config.js            # Tailwind CSS 配置
├── server.js                     # Fastify 服務器
└── package.json                  # 專案依賴
```

## 🛠️ 技術棧

- **Eleventy (11ty)** - 靜態網站生成器
- **Nunjucks** - 模板引擎
- **Tailwind CSS** - 實用優先的 CSS 框架
- **Fastify** - 高性能 Node.js 服務器
- **Google Fonts** - Inter 和 Anton 字體
- **Vanilla JavaScript** - 原生 JavaScript 互動功能

## 📦 產品系列

### 🔋 Power Pro Series
- **Power Pro 10000mAh** - 高容量行動電源
- **Power PD** - 快充技術支援

### 🌱 Loopenergy Series
- **Loopenergy 10000mAh** - 環保永續行動電源
- **Loopenergy 5000mAh** - 輕巧環保電源

### ⚡ GaN MOJO Series
- **MOJO 140W GaN Charger** - 超快充電器
- **MOJO 65W GaN Charger** - 高效能充電器

### 💾 Memory Series
- **USB 3.0 64GB** - 高速隨身碟
- **Flash Disk** - 記憶體儲存解決方案

## 🚀 安裝和運行

### 前置需求

- Node.js (版本 18 或更高)
- npm

### 安裝步驟

1. **克隆專案**
   ```bash
   git clone <repository-url>
   cd verico
   ```

2. **安裝依賴**
   ```bash
   npm install
   ```

3. **開發模式**
   ```bash
   npm run dev
   ```
   這會啟動本地開發服務器，通常在 `http://localhost:8080`

4. **建置生產版本**
   ```bash
   npm run build
   ```
   這會在 `_site` 目錄生成靜態文件

5. **啟動生產服務器**
   ```bash
   npm run fastify
   ```

## 🔧 開發腳本

- `npm run dev` - 啟動開發服務器（熱重載）
- `npm run build` - 建置生產版本
- `npm run serve` - 啟動服務器（無熱重載）
- `npm run fastify` - 使用 Fastify 啟動服務器
- `npm run static` - 啟動 Python 靜態文件服務器

## 📝 自定義配置

### 修改網站內容

編輯 `src/_data/site.json` 文件來更新網站資訊：

```json
{
  "company": {
    "name": "Verico",
    "tagline": "We care & We share"
  },
  "hero": {
    "title": "Charge Ahead.\nStore Smart.",
    "image": "/assets/images/banner/hero/hero-image.jpg"
  }
}
```

### 修改產品資料

編輯 `src/_data/products.json` 文件來管理產品資訊：

```json
{
  "products": {
    "product-id": {
      "name": "產品名稱",
      "description": "產品描述",
      "specs": {
        "power": "功率規格"
      }
    }
  }
}
```

### 修改樣式

編輯 `src/assets/css/tailwind.css` 來自定義 Tailwind CSS：

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* 自定義樣式 */
```

## 🌐 部署選項

### 靜態主機服務

建置完成後，將 `_site` 目錄的內容上傳到任何靜態主機服務：

- **Netlify** - 推薦，支援自動部署
- **Vercel** - 快速部署和 CDN
- **GitHub Pages** - 免費靜態託管
- **AWS S3** - 企業級解決方案

### 本地測試

```bash
npm run build
npx serve _site
```

## 🎨 設計特色

- **玻璃態效果** - 現代化的毛玻璃設計
- **響應式佈局** - 完美適配各種設備
- **低飽和度色彩** - 專業的企業風格
- **精確網格對齊** - 簡潔的視覺效果
- **類似 Linear 風格** - 現代化的企業網站設計

## 🔄 開發工作流程

1. **內容更新** - 修改 `src/_data/` 中的 JSON 文件
2. **樣式調整** - 編輯 Tailwind CSS 類別
3. **模板修改** - 更新 `src/_includes/` 中的模板
4. **即時預覽** - 開發服務器自動重新載入
5. **建置部署** - 生成靜態文件並部署

## 📞 聯絡資訊

- **公司理念**: We care & We share
- **產品特色**: ECO not EGO
- **技術支援**: 提供完整的技術支援服務

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

## 📄 授權

MIT License 