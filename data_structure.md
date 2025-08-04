# 數據目錄結構重構指南

## 🎯 重構目標

將原本扁平化的 `_data` 目錄重構為更有組織性的結構，提高可維護性和可讀性。

## 📁 新的目錄結構

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

## 🔧 配置更新

### Eleventy 配置 (.eleventy.js)

新的配置自動處理數據載入：

```javascript
// 網站配置
eleventyConfig.addGlobalData("site", () => {
  const siteConfigPath = "src/_data/site/config.yml";
  if (fs.existsSync(siteConfigPath)) {
    return yaml.load(fs.readFileSync(siteConfigPath, "utf8"));
  }
  return {};
});

// 導航數據
eleventyConfig.addGlobalData("navigation", () => {
  const navConfigPath = "src/_data/site/navigation.yml";
  if (fs.existsSync(navConfigPath)) {
    return yaml.load(fs.readFileSync(navConfigPath, "utf8"));
  }
  return {};
});

// 內容數據
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
```

## 📝 模板中的數據引用

### 向後兼容的引用方式

為了保持現有模板正常工作，保留了舊的數據引用：

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

### 新的引用方式（推薦）

```nunjucks
<!-- 使用新的 content 結構 -->
{% set data = content.homepage.en %}  <!-- 英文首頁 -->
{% set data = content.homepage.de %}  <!-- 德文首頁 -->

{% set data = content.contact.en %}   <!-- 英文聯繫頁面 -->
{% set data = content.contact.de %}   <!-- 德文聯繫頁面 -->

{% set data = content.products.en %}  <!-- 英文產品目錄 -->
{% set data = content.products.de %}  <!-- 德文產品目錄 -->
```

## 🎯 優勢

### 1. **清晰的組織結構**
- 按功能分組：`site/`, `content/`, `shared/`
- 按內容類型分組：`homepage/`, `contact/`, `products/`
- 按語言分組：`en.yml`, `de.yml`

### 2. **易於維護**
- 相關文件集中在一起
- 新增產品只需在 `products/details/` 下創建新目錄
- 語言版本並列，便於對比和更新

### 3. **可擴展性**
- 新增頁面類型只需在 `content/` 下創建新目錄
- 新增語言只需在每個目錄下添加對應的 `.yml` 文件
- 新增產品只需在 `products/details/` 下創建新目錄

### 4. **向後兼容**
- 保留了舊的數據引用方式
- 現有模板無需修改即可正常工作
- 可以逐步遷移到新的引用方式

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

## 🔄 遷移計劃

### 第一階段：結構重構 ✅
- [x] 創建新的目錄結構
- [x] 移動現有文件
- [x] 更新 Eleventy 配置
- [x] 測試向後兼容性

### 第二階段：模板更新（可選）
- [ ] 逐步更新模板使用新的 `content` 結構
- [ ] 移除舊的數據引用
- [ ] 優化數據載入邏輯

### 第三階段：功能擴展
- [ ] 添加更多產品詳情頁面
- [ ] 實現動態產品數據載入
- [ ] 添加內容管理工具

這個新的結構大大提高了項目的可維護性和可擴展性！ 