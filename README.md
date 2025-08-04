# Verico 企業網站

基於 Eleventy (11ty) 靜態網站生成器構建的現代化企業網站，支持多語言（英文/德文）和響應式設計。

## 🚀 快速開始

### 環境要求
- Node.js 18+
- npm 或 yarn

### 安裝和運行
```bash
# 安裝依賴
npm install

# 開發模式
npm run dev

# 構建生產版本
npm run build
```

## 📁 項目結構

```
verico/
├── src/
│   ├── _data/                    # 數據文件
│   │   ├── site/                 # 網站配置
│   │   │   ├── config.yml        # 網站全局配置
│   │   │   └── navigation.yml    # 導航數據
│   │   ├── content/              # 內容數據
│   │   │   ├── homepage/         # 首頁內容
│   │   │   │   ├── en.yml       # 英文首頁
│   │   │   │   └── de.yml       # 德文首頁
│   │   │   ├── contact/          # 聯繫頁面
│   │   │   │   ├── en.yml       # 英文聯繫頁面
│   │   │   │   └── de.yml       # 德文聯繫頁面
│   │   │   └── products/         # 產品相關
│   │   │       ├── catalog/      # 產品目錄
│   │   │       │   ├── en.yml   # 英文產品目錄
│   │   │       │   └── de.yml   # 德文產品目錄
│   │   │       └── details/      # 產品詳情
│   │   │           └── mojo-140w-gan-charger/
│   │   │               ├── en.yml # 英文產品詳情
│   │   │               └── de.yml # 德文產品詳情
│   │   └── shared/               # 共享數據
│   ├── _includes/                # 模板組件
│   │   ├── layout.njk           # 主布局
│   │   ├── nav.njk              # 導航組件
│   │   ├── footer.njk           # 頁腳組件
│   │   └── language-switcher.njk # 語言切換器
│   ├── en/                      # 英文頁面
│   │   ├── index.njk            # 英文首頁
│   │   ├── contact.njk          # 英文聯繫頁面
│   │   └── products/            # 英文產品頁面
│   ├── de/                      # 德文頁面
│   │   ├── index.njk            # 德文首頁
│   │   ├── contact.njk          # 德文聯繫頁面
│   │   └── products/            # 德文產品頁面
│   ├── index.njk                # 智能跳轉頁面
│   └── assets/                  # 靜態資源
│       ├── css/
│       ├── js/
│       └── images/
├── _site/                       # 構建輸出
├── .eleventy.js                 # Eleventy 配置
├── package.json
└── README.md
```

## 🎯 核心功能

### 1. 多語言支持
- **智能語言檢測**：根據用戶地區和瀏覽器語言自動選擇語言
- **Cookie 記憶**：記住用戶語言偏好
- **手動語言切換**：右上角語言切換器
- **完全分離的數據**：英文和德文內容獨立維護

### 2. 多語言導航系統 🆕

#### 多語言 URL 結構
```yaml
# src/_data/site/navigation.yml
main:
  - title:
      en: Products
      de: Produkte
    url:
      en: /en/products/
      de: /de/products/
    submenu:
      - title:
          en: Power Pro 20000mAh
          de: Power Pro 20000mAh
        url:
          en: /en/products/powerbank/power-pro-20000mah
          de: /de/products/powerbank/power-pro-20000mah
        available_in: [en]  # 只有英文版顯示
```

#### 條件顯示控制
- **`available_in: [en]`**：只有英文版顯示
- **`available_in: [de]`**：只有德文版顯示  
- **`available_in: [en, de]`**：兩種語言都顯示

#### 模板支援
```nunjucks
<!-- 桌面版導航 -->
{% for nav in navigation.main %}
  {% if not nav.available_in or lang in nav.available_in %}
    <a href="{{ nav.url[lang] or nav.url.en }}">
      {{ nav.title[lang] or nav.title.en }}
    </a>
  {% endif %}
{% endfor %}
```

### 3. 數據管理架構

#### 重構後的數據結構
將原本扁平化的 `_data` 目錄重構為更有組織性的結構：

```
src/_data/
├── site/                          # 網站配置
│   ├── config.yml                 # 網站全局配置
│   └── navigation.yml             # 導航數據
├── content/                       # 內容數據
│   ├── homepage/                  # 首頁內容
│   │   ├── en.yml                # 英文首頁
│   │   └── de.yml                # 德文首頁
│   ├── contact/                   # 聯繫頁面
│   │   ├── en.yml                # 英文聯繫頁面
│   │   └── de.yml                # 德文聯繫頁面
│   └── products/                  # 產品相關
│       ├── catalog/               # 產品目錄
│       │   ├── en.yml            # 英文產品目錄
│       │   └── de.yml            # 德文產品目錄
│       └── details/               # 產品詳情
│           └── mojo-140w-gan-charger/
│               ├── en.yml         # 英文產品詳情
│               └── de.yml         # 德文產品詳情
└── shared/                        # 共享數據
    └── common.yml                 # 通用數據
```

#### 優勢
- **✅ 清晰的組織結構** - 按功能和內容類型分組
- **✅ 易於維護** - 相關文件集中，語言版本並列
- **✅ 高度可擴展** - 新增產品/頁面/語言都很簡單
- **✅ 向後兼容** - 現有模板無需修改即可工作

### 4. 首頁處理方式

#### 智能跳轉機制
創建了 `src/index.njk` 作為根目錄跳轉頁面：

```html
---
layout: layout.njk
title: Redirecting...
permalink: /
---

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Redirecting...</title>
    <!-- 載入動畫樣式 -->
</head>
<body>
    <div class="loader">
        <div class="spinner"></div>
        <p>Detecting your location...</p>
    </div>

    <script>
        // 檢查是否已有語言偏好 cookie
        function getCookie(name) {
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) return parts.pop().split(';').shift();
        }

        // 獲取用戶的語言偏好
        function getUserLanguage() {
            // 首先檢查 cookie
            const savedLang = getCookie('preferred_language');
            if (savedLang) {
                return savedLang;
            }

            // 檢查瀏覽器語言
            const browserLang = navigator.language || navigator.userLanguage;
            
            // 德國、奧地利、瑞士等德語國家
            const germanCountries = ['de', 'at', 'ch', 'li', 'lu'];
            const countryCode = browserLang.split('-')[1]?.toLowerCase();
            
            if (germanCountries.includes(countryCode) || browserLang.startsWith('de')) {
                return 'de';
            }
            
            // 默認使用英文
            return 'en';
        }

        // 設置 cookie 並跳轉
        function redirectToLanguage() {
            const lang = getUserLanguage();
            
            // 設置 cookie (30天過期)
            const expiryDate = new Date();
            expiryDate.setDate(expiryDate.getDate() + 30);
            document.cookie = `preferred_language=${lang}; expires=${expiryDate.toUTCString()}; path=/`;
            
            // 跳轉到相應語言版本
            window.location.href = `/${lang}/`;
        }

        // 延遲一點時間讓用戶看到載入動畫
        setTimeout(redirectToLanguage, 1500);
    </script>
</body>
</html>
```

#### 工作流程
1. **首次訪問**：
   - 用戶訪問 `http://localhost:8080/`
   - 系統檢測用戶地區/瀏覽器語言
   - 自動跳轉到 `/en/` 或 `/de/`
   - 設置 `preferred_language` cookie

2. **後續訪問**：
   - 檢查 cookie 中的語言偏好
   - 直接跳轉到相應語言版本

3. **手動切換**：
   - 右上角的語言切換器
   - 點擊可切換語言並更新 cookie

### 5. 數據引用方式

#### 向後兼容的引用方式
```nunjucks
<!-- 首頁數據 -->
{% set data = homepageen %}  <!-- 英文 -->
{% set data = homepagede %}  <!-- 德文 -->

<!-- 聯繫頁面數據 -->
{% set data = contact.en %}  <!-- 英文 -->
{% set data = contact.de %}  <!-- 德文 -->

<!-- 產品數據 -->
{% set data = products.en %} <!-- 英文 -->
{% set data = products.de %} <!-- 德文 -->

<!-- 網站配置 -->
{{ site.name }}
{{ site.url }}

<!-- 導航數據 -->
{% for nav in navigation.main %}
```

#### 新的引用方式（推薦）
```nunjucks
<!-- 使用新的 content 結構 -->
{% set data = content.homepage.en %}  <!-- 英文首頁 -->
{% set data = content.homepage.de %}  <!-- 德文首頁 -->

{% set data = content.contact.en %}   <!-- 英文聯繫頁面 -->
{% set data = content.contact.de %}   <!-- 德文聯繫頁面 -->

{% set data = content.products.en %}  <!-- 英文產品目錄 -->
{% set data = content.products.de %}  <!-- 德文產品目錄 -->
```

## 🔧 配置說明

### Eleventy 配置 (.eleventy.js)
更新了配置以支持新的數據目錄結構：

```javascript
// 數據處理邏輯
eleventyConfig.addGlobalData("site", () => {
  const siteConfigPath = "src/_data/site/config.yml";
  if (fs.existsSync(siteConfigPath)) {
    return yaml.load(fs.readFileSync(siteConfigPath, "utf8"));
  }
  return {};
});

eleventyConfig.addGlobalData("navigation", () => {
  const navConfigPath = "src/_data/site/navigation.yml";
  if (fs.existsSync(navConfigPath)) {
    return yaml.load(fs.readFileSync(navConfigPath, "utf8"));
  }
  return {};
});

// 處理內容數據
eleventyConfig.addGlobalData("content", () => {
  const contentData = {};
  
  // 處理首頁數據
  languages.forEach(lang => {
    const homepagePath = `src/_data/content/homepage/${lang}.yml`;
    if (fs.existsSync(homepagePath)) {
      if (!contentData.homepage) contentData.homepage = {};
      contentData.homepage[lang] = yaml.load(fs.readFileSync(homepagePath, "utf8"));
    }
  });

  // 處理聯繫頁面數據
  languages.forEach(lang => {
    const contactPath = `src/_data/content/contact/${lang}.yml`;
    if (fs.existsSync(contactPath)) {
      if (!contentData.contact) contentData.contact = {};
      contentData.contact[lang] = yaml.load(fs.readFileSync(contactPath, "utf8"));
    }
  });

  // 處理產品目錄數據
  languages.forEach(lang => {
    const productsPath = `src/_data/content/products/catalog/${lang}.yml`;
    if (fs.existsSync(productsPath)) {
      if (!contentData.products) contentData.products = {};
      contentData.products[lang] = yaml.load(fs.readFileSync(productsPath, "utf8"));
    }
  });

  return contentData;
});

// 為了向後兼容，保留舊的數據引用
eleventyConfig.addGlobalData("homepageen", () => {
  const path = "src/_data/content/homepage/en.yml";
  if (fs.existsSync(path)) {
    return yaml.load(fs.readFileSync(path, "utf8"));
  }
  return {};
});

eleventyConfig.addGlobalData("homepagede", () => {
  const path = "src/_data/content/homepage/de.yml";
  if (fs.existsSync(path)) {
    return yaml.load(fs.readFileSync(path, "utf8"));
  }
  return {};
});
```

## 📋 維護指南

### 添加新產品
1. 在 `src/_data/content/products/details/` 下創建產品目錄
2. 在產品目錄下創建 `en.yml` 和 `de.yml`
3. 更新導航數據 `src/_data/site/navigation.yml`

### 添加新頁面類型
1. 在 `src/_data/content/` 下創建新目錄
2. 在新目錄下創建 `en.yml` 和 `de.yml`
3. 更新 Eleventy 配置以載入新數據

### 添加新語言
1. 在每個內容目錄下添加新的語言文件（如 `fr.yml`）
2. 更新 Eleventy 配置中的語言列表
3. 更新導航數據

### 多語言導航管理 🆕

#### 添加新產品到導航
```yaml
# src/_data/site/navigation.yml
submenu:
  - title:
      en: New Product
      de: Neues Produkt
    url:
      en: /en/products/new-product
      de: /de/products/new-product
    available_in: [en, de]  # 兩種語言都顯示
```

#### 控制產品顯示
```yaml
# 只有英文版顯示
available_in: [en]

# 只有德文版顯示  
available_in: [de]

# 兩種語言都顯示
available_in: [en, de]

# 所有語言都顯示（不設置 available_in）
```

## 🎨 設計特色

- **現代化設計**：採用 Tailwind CSS 框架
- **響應式布局**：適配桌面、平板、手機
- **優雅動畫**：載入動畫和過渡效果
- **無障礙設計**：符合 WCAG 標準

## 📚 相關文檔

- [數據結構重構指南](data_structure.md)
- [Homepage 問題解決方案](homepage_issue.md)
- [圖片路徑問題解決方案](image_issue.md)

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

## �� 許可證

MIT License 