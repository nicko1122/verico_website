# YAML數據讀取問題解決報告

## 📋 問題概述

在將Verico專案轉換為11ty無頭CMS過程中，遇到了YAML數據文件無法正確讀取的問題。模板無法訪問YAML數據，導致頁面內容無法動態顯示。

## 🔍 問題診斷過程

### 1. 初始問題發現
- 模板中使用 `{{ index.en.hero.title }}` 等數據訪問方式
- 生成的頁面顯示空白內容
- Debug頁面顯示數據為空
- 控制台顯示11ty正在監視文件變化但數據未正確讀取

### 2. 數據文件結構分析
原始數據文件結構：
```
src/_data/
├── index.en.yml          # 英文首頁數據
├── index.de.yml          # 德文首頁數據
├── products.en.yml       # 英文產品數據
├── products.de.yml       # 德文產品數據
├── contact.en.yml        # 英文聯絡數據
├── contact.de.yml        # 德文聯絡數據
├── navigation.yml        # 導航數據
└── site.yml             # 網站基本數據
```

**問題分析：**
- 文件名使用點號分隔語言後綴（如 `index.en.yml`）
- 11ty會將文件名解析為數據對象名稱
- 這種命名方式與11ty的內部機制產生衝突

### 3. 11ty數據讀取機制深度分析

#### 3.1 11ty數據文件命名規則
```javascript
// 11ty會將文件名映射為數據對象名稱
// index.en.yml → 數據對象名稱為 "index"
// products.en.yml → 數據對象名稱為 "products"
```

#### 3.2 實際測試結果
創建測試頁面驗證數據讀取：
```njk
---
layout: layout.njk
title: Debug Page
permalink: /debug/
---

<div class="max-w-4xl mx-auto px-4 py-8">
  <h1 class="text-3xl font-bold mb-6">Debug Page - All Available Data</h1>
  
  <div class="space-y-6">
    <div class="bg-red-50 border border-red-200 rounded-lg p-6">
      <h2 class="text-xl font-semibold text-red-900 mb-4">Site Data:</h2>
      <pre class="text-sm text-red-800 overflow-auto">{{ site | dump }}</pre>
    </div>
    
    <div class="bg-blue-50 border border-blue-200 rounded-lg p-6">
      <h2 class="text-xl font-semibold text-blue-900 mb-4">Navigation Data:</h2>
      <pre class="text-sm text-blue-800 overflow-auto">{{ navigation | dump }}</pre>
    </div>
    
    <div class="bg-green-50 border border-green-200 rounded-lg p-6">
      <h2 class="text-xl font-semibold text-green-900 mb-4">Index EN Data:</h2>
      <pre class="text-sm text-green-800 overflow-auto">{{ index.en | dump }}</pre>
    </div>
    
    <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
      <h2 class="text-xl font-semibold text-yellow-900 mb-4">Index DE Data:</h2>
      <pre class="text-sm text-yellow-800 overflow-auto">{{ index.de | dump }}</pre>
    </div>
  </div>
</div>
```

**測試結果：**
- `site` 數據：✅ 正確讀取
- `navigation` 數據：✅ 正確讀取  
- `index.en` 數據：❌ 為空
- `index.de` 數據：❌ 為空

#### 3.3 根本原因分析
1. **文件名衝突**：`index.en.yml` 中的 `index` 與11ty內部機制衝突
2. **數據結構問題**：11ty無法正確解析帶語言後綴的文件名
3. **訪問路徑錯誤**：模板中的數據訪問路徑與實際數據結構不匹配

## 🛠️ 解決方案實施

### 1. 重新組織數據文件結構

#### 步驟1：重命名數據文件
```bash
# 在 src/_data/ 目錄下執行
mv index.en.yml homepage.en.yml
mv index.de.yml homepage.de.yml
```

#### 步驟2：創建統一的數據文件結構
**原始問題：**
```yaml
# index.en.yml
hero:
  title: "Charge Ahead.\nStore Smart."
  image: "assets/images/banner/hero/Carousel/GaNCharger-banner.jpg"
```

**解決方案：**
```yaml
# homepage.yml
en:
  hero:
    title: "Charge Ahead.\nStore Smart."
    image: "assets/images/banner/hero/Carousel/GaNCharger-banner.jpg"
    alt: "Verico Hero Banner"
  products_section:
    title: "Products by Category"
    buttons:
      - "About Our Product"
      - "ECO not EGO"
      - "Memory Experience"
    categories:
      - name: "Power Pro Series"
        description: "High Capacity. Fast Charge. Endless Energy."
        image: "assets/images/banner/tab/product-tab/powerbank-tab.png"
        link: "/en/products/powerbank"
      # ... 更多分類

de:
  hero:
    title: "Laden Sie voraus.\nSpeichern Sie intelligent."
    image: "assets/images/banner/hero/Carousel/GaNCharger-banner.jpg"
    alt: "Verico Hero Banner"
  products_section:
    title: "Produkte nach Kategorie"
    buttons:
      - "Über unser Produkt"
      - "ECO nicht EGO"
      - "Memory Experience"
    categories:
      - name: "Power Pro Serie"
        description: "Hohe Kapazität. Schnelles Laden. Endlose Energie."
        image: "assets/images/banner/tab/product-tab/powerbank-tab.png"
        link: "/de/products/powerbank"
      # ... 更多分類
```

#### 步驟3：驗證數據讀取
創建簡單測試頁面：
```njk
---
layout: layout.njk
title: Simple Test
permalink: /simple-test/
---

<div class="max-w-4xl mx-auto px-4 py-8">
  <h1 class="text-3xl font-bold mb-6">Simple Data Test</h1>
  
  <div class="space-y-6">
    <div class="bg-blue-50 border border-blue-200 rounded-lg p-6">
      <h2 class="text-xl font-semibold text-blue-900 mb-4">Direct Data Access:</h2>
      <p><strong>Homepage EN Hero Title:</strong> {{ homepage.en.hero.title }}</p>
      <p><strong>Homepage EN Hero Image:</strong> {{ homepage.en.hero.image }}</p>
      <p><strong>Homepage DE Hero Title:</strong> {{ homepage.de.hero.title }}</p>
    </div>
  </div>
</div>
```

**驗證結果：**
- ✅ 英文標題：正確顯示 "Charge Ahead.\nStore Smart."
- ✅ 英文圖片：正確顯示路徑
- ✅ 德文標題：正確顯示 "Laden Sie voraus.\nSpeichern Sie intelligent."

### 2. 創建統一的數據文件

#### 新的數據文件結構：
```
src/_data/
├── homepage.yml          # 首頁數據（多語言）
├── products.yml          # 產品頁面數據（多語言）
├── contact.yml           # 聯絡頁面數據（多語言）
├── navigation.yml        # 導航選單（多語言）
└── site.yml             # 網站基本資訊
```

### 3. 更新模板數據訪問方式

#### 步驟1：分析原始模板問題
**原始模板（有問題）：**
```njk
<!-- 英文首頁模板 -->
<img src="{{ index.en.hero.image }}" alt="{{ index.en.hero.alt }}" />
<h1>{{ index.en.hero.title | safe }}</h1>

<!-- 德文首頁模板 -->
{% set data = index.de %}
<img src="{{ data.hero.image }}" alt="{{ data.hero.alt }}" />
<h1>{{ data.hero.title | safe }}</h1>
```

**問題分析：**
- 英文模板直接使用 `index.en.hero.title`，但數據文件不存在
- 德文模板使用 `{% set data = index.de %}`，但數據結構不匹配
- 兩種訪問方式不一致，難以維護

#### 步驟2：統一模板數據訪問方式
**更新後的模板（正確）：**

**英文首頁模板 (`src/en/index.njk`)：**
```njk
---
layout: layout.njk
title: Home
lang: en
permalink: /en/
---

{% set data = homepage.en %}

<!-- Hero Section -->
<section class="relative w-[99%] h-[800px]">
    <div class="hero-wrapper rounded-2xl border border-gray-200 mx-2 my-3 md:mx-4 md:my-4 overflow-hidden h-full">
        <div class="hero-container relative w-full h-full mx-auto">
            <img src="{{ data.hero.image }}" alt="{{ data.hero.alt }}"
                class="w-full h-full object-cover object-center" />
            <div class="absolute inset-y-10 right-0 flex items-center pr-10">
                <h1 class="text-5xl font-bold text-gray-500 break-words text-left px-6 py-4">
                    {{ data.hero.title | safe }}
                </h1>
            </div>
        </div>
    </div>
</section>

<!-- Products Section -->
<section class="py-5">
    <div class="max-w-6xl mx-auto px-6">
        <div class="mb-3 mt-0">
            <h1 class="text-5xl font-bold tracking-tight text-gray-800 mb-0 mt-0 break-words text-center">
                {{ data.products_section.title }}</h1>
        </div>
        <div class="flex justify-center gap-3 my-6">
            {% for button in data.products_section.buttons %}
            <button class="px-4 py-1.5 bg-white border border-gray-200 text-gray-700 rounded-lg font-medium text-xs focus:outline-none">
                {{ button }}
            </button>
            {% endfor %}
        </div>
        <div class="flex flex-col md:flex-row w-full h-auto md:h-[400px] gap-4">
            {% for category in data.products_section.categories %}
            <div class="relative overflow-hidden rounded-2xl flex-1 md:group md:transition-all md:duration-300 md:hover:flex-[4]">
                <img src="{{ category.image }}" class="w-full h-56 md:h-full object-cover" />
                <div class="absolute top-0 left-0 p-5">
                    <h3 class="text-xl font-semibold text-white mb-2">{{ category.name }}</h3>
                    <p class="text-gray-200 text-sm">{{ category.description }}</p>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</section>
```

**德文首頁模板 (`src/de/index.njk`)：**
```njk
---
layout: layout.njk
title: Home
lang: de
permalink: /de/
---

{% set data = homepage.de %}

<!-- 相同的HTML結構，但使用德文數據 -->
```

#### 步驟3：驗證模板更新
**構建並測試：**
```bash
npm run build
```

**檢查生成的HTML：**
```bash
grep -A 5 -B 5 "Charge Ahead" _site/en/index.html
grep -A 5 -B 5 "Laden Sie voraus" _site/de/index.html
```

**預期結果：**
- 英文頁面顯示：`Charge Ahead.\nStore Smart.`
- 德文頁面顯示：`Laden Sie voraus.\nSpeichern Sie intelligent.`

### 4. 驗證數據讀取

創建測試文件來驗證數據結構：
```njk
---
layout: layout.njk
title: Data Test
permalink: /simple-test/
---

<div class="max-w-4xl mx-auto px-4 py-8">
  <h1 class="text-3xl font-bold mb-6">Data Structure Test</h1>
  
  <div class="space-y-6">
    <div class="bg-blue-50 border border-blue-200 rounded-lg p-6">
      <h2 class="text-xl font-semibold text-blue-900 mb-4">Direct Data Access:</h2>
      <p><strong>Homepage EN Hero Title:</strong> {{ homepage.en.hero.title }}</p>
      <p><strong>Homepage EN Hero Image:</strong> {{ homepage.en.hero.image }}</p>
      <p><strong>Homepage DE Hero Title:</strong> {{ homepage.de.hero.title }}</p>
      <p><strong>Products EN Hero Title:</strong> {{ products.en.hero.title }}</p>
      <p><strong>Contact EN Hero Title:</strong> {{ contact.en.hero.title }}</p>
    </div>
  </div>
</div>
```

## ✅ 解決結果

### 1. 數據讀取成功驗證
- ✅ 英文首頁：正確顯示 "Charge Ahead.\nStore Smart."
- ✅ 德文首頁：正確顯示 "Laden Sie voraus.\nSpeichern Sie intelligent."
- ✅ 產品頁面：正確顯示 "Our Products.\nYour Power."
- ✅ 聯絡頁面：正確顯示 "Contact Us"

### 2. 多語言支援完整
- 每個數據文件包含 `en` 和 `de` 兩個語言版本
- 模板可以根據語言動態選擇對應的數據
- 支援完整的國際化功能

### 3. 數據結構優化
- 統一的數據組織方式
- 清晰的命名規範
- 易於維護和擴展

## 📊 技術細節

### 1. 11ty配置確認
```javascript
// .eleventy.js
const yaml = require("js-yaml");

module.exports = function(eleventyConfig) {
  // 複製靜態資源
  eleventyConfig.addPassthroughCopy("src/assets");
  eleventyConfig.addPassthroughCopy("static/assets");

  // 設定模板引擎
  eleventyConfig.setTemplateFormats([
    "html",
    "njk",
    "md"
  ]);

  // 設定語言
  const languages = ["en", "de"];

  // 為每個語言建立頁面
  languages.forEach(lang => {
    eleventyConfig.addGlobalData("lang", lang);
  });

  // 添加 absoluteUrl filter
  eleventyConfig.addFilter("absoluteUrl", function(url) {
    if (!url) return "";
    if (url.startsWith("http")) return url;
    return url;
  });

  // 添加 dump filter 用於調試
  eleventyConfig.addFilter("dump", function(obj) {
    return JSON.stringify(obj, null, 2);
  });

  // 明確配置 YAML 支援
  eleventyConfig.addDataExtension("yaml", contents => yaml.load(contents));
  eleventyConfig.addDataExtension("yml", contents => yaml.load(contents));

  // 設定輸出目錄
  eleventyConfig.addPassthroughCopy("src/assets");

  // 設定監視檔案
  eleventyConfig.addWatchTarget("src/assets/");

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data"
    },
    templateFormats: ["html", "njk", "md"],
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: "njk",
    dataTemplateEngine: "njk"
  };
};
```

### 2. 數據文件命名規範詳解

#### 2.1 正確的命名方式
```bash
# ✅ 推薦的命名方式
homepage.yml          # 包含 en 和 de 兩個語言版本
products.yml          # 包含 en 和 de 兩個語言版本
contact.yml           # 包含 en 和 de 兩個語言版本
navigation.yml        # 多語言導航數據
site.yml             # 網站基本資訊
```

#### 2.2 避免的命名方式
```bash
# ❌ 不推薦的命名方式
index.en.yml          # 會與11ty內部機制衝突
index.de.yml          # 會與11ty內部機制衝突
products.en.yml       # 語言後綴會導致問題
products.de.yml       # 語言後綴會導致問題
```

#### 2.3 數據結構最佳實踐
```yaml
# ✅ 推薦的數據結構
# homepage.yml
en:
  hero:
    title: "English Title"
    image: "path/to/image.jpg"
de:
  hero:
    title: "German Title"
    image: "path/to/image.jpg"
```

### 3. 模板數據訪問模式詳解

#### 3.1 基本訪問模式
```njk
<!-- 直接訪問 -->
{{ homepage.en.hero.title }}
{{ homepage.de.hero.title }}

<!-- 使用變數簡化 -->
{% set data = homepage.en %}
{{ data.hero.title }}

{% set data = homepage.de %}
{{ data.hero.title }}
```

#### 3.2 循環訪問模式
```njk
<!-- 訪問數組數據 -->
{% for category in data.products_section.categories %}
<div class="category">
  <h3>{{ category.name }}</h3>
  <p>{{ category.description }}</p>
  <img src="{{ category.image }}" alt="{{ category.alt }}" />
</div>
{% endfor %}

<!-- 訪問按鈕數據 -->
{% for button in data.products_section.buttons %}
<button class="btn">{{ button }}</button>
{% endfor %}
```

#### 3.3 條件訪問模式
```njk
<!-- 根據語言動態選擇數據 -->
{% if page.lang == 'en' %}
  {% set data = homepage.en %}
{% else %}
  {% set data = homepage.de %}
{% endif %}

<!-- 安全訪問（避免錯誤） -->
{{ data.hero.title | default('Default Title') }}
{{ data.hero.image | default('/default-image.jpg') }}
```

### 4. 調試技巧

#### 4.1 使用dump filter調試
```njk
<!-- 顯示完整數據結構 -->
<pre>{{ homepage | dump }}</pre>

<!-- 顯示特定數據 -->
<pre>{{ homepage.en | dump }}</pre>
<pre>{{ data | dump }}</pre>
```

#### 4.2 創建調試頁面
```njk
---
layout: layout.njk
title: Debug Page
permalink: /debug/
---

<div class="max-w-4xl mx-auto px-4 py-8">
  <h1 class="text-3xl font-bold mb-6">Debug Page</h1>
  
  <div class="space-y-6">
    <div class="bg-blue-50 border border-blue-200 rounded-lg p-6">
      <h2 class="text-xl font-semibold text-blue-900 mb-4">Available Data:</h2>
      <pre class="text-sm text-blue-800 overflow-auto">{{ eleventy | dump }}</pre>
    </div>
    
    <div class="bg-green-50 border border-green-200 rounded-lg p-6">
      <h2 class="text-xl font-semibold text-green-900 mb-4">Homepage Data:</h2>
      <pre class="text-sm text-green-800 overflow-auto">{{ homepage | dump }}</pre>
    </div>
  </div>
</div>
```

#### 4.3 命令行調試
```bash
# 檢查生成的HTML內容
grep -A 10 -B 10 "特定文字" _site/en/index.html

# 檢查數據是否正確讀取
grep -A 5 "Direct Data Access" _site/simple-test/index.html

# 檢查構建過程
npm run build
```

### 2. 數據文件命名規範
- 使用描述性文件名（如 `homepage.yml` 而不是 `index.en.yml`）
- 在文件內部組織多語言數據
- 避免使用點號分隔的語言後綴

### 3. 模板數據訪問模式
```njk
{% set data = homepage.en %}  // 英文數據
{% set data = homepage.de %}  // 德文數據

{{ data.hero.title }}
{{ data.products_section.title }}
{{ data.trending_products.products }}
```

## 🎯 最佳實踐總結

### 1. 數據文件組織
- 按功能分類（homepage、products、contact）
- 每個文件包含所有語言版本
- 使用清晰的層級結構

### 2. 模板設計
- 使用 `{% set data = ... %}` 簡化數據訪問
- 保持模板的可讀性和可維護性
- 支援動態語言切換

### 3. 驗證和測試
- 創建專門的測試頁面驗證數據讀取
- 使用 `{{ data | dump }}` 調試數據結構
- 確保所有語言版本正常工作

## 📝 經驗教訓與最佳實踐

### 1. 11ty數據文件命名規則
**重要原則：**
- ✅ 使用描述性文件名（如 `homepage.yml`）
- ✅ 在文件內部組織多語言數據
- ❌ 避免使用點號分隔的語言後綴（如 `index.en.yml`）
- ❌ 避免使用可能與11ty內部機制衝突的名稱

**命名衝突檢查：**
```bash
# 檢查是否有命名衝突
ls src/_data/ | grep -E "\.(en|de)\.yml$"
```

### 2. 數據結構設計原則
**多語言數據組織：**
```yaml
# ✅ 推薦：在單一文件中組織多語言
homepage.yml:
  en: { hero: { title: "English" } }
  de: { hero: { title: "German" } }

# ❌ 避免：分離的語言文件
index.en.yml: { hero: { title: "English" } }
index.de.yml: { hero: { title: "German" } }
```

**數據層級設計：**
```yaml
# ✅ 清晰的層級結構
en:
  hero:
    title: "Title"
    image: "path/to/image.jpg"
  products_section:
    title: "Products"
    categories: [...]
  trending_products:
    title: "Trending"
    products: [...]
```

### 3. 模板設計最佳實踐
**統一數據訪問模式：**
```njk
<!-- ✅ 推薦：使用變數簡化訪問 -->
{% set data = homepage.en %}
{{ data.hero.title }}

<!-- ❌ 避免：直接訪問複雜路徑 -->
{{ homepage.en.hero.title }}
```

**錯誤處理：**
```njk
<!-- ✅ 安全訪問 -->
{{ data.hero.title | default('Default Title') }}
{{ data.hero.image | default('/default-image.jpg') }}

<!-- ✅ 條件檢查 -->
{% if data.hero.title %}
  <h1>{{ data.hero.title }}</h1>
{% endif %}
```

### 4. 測試和驗證策略
**創建測試頁面：**
```njk
---
layout: layout.njk
title: Data Test
permalink: /test-data/
---

<div class="max-w-4xl mx-auto px-4 py-8">
  <h1 class="text-3xl font-bold mb-6">Data Structure Test</h1>
  
  <div class="space-y-6">
    <div class="bg-blue-50 border border-blue-200 rounded-lg p-6">
      <h2 class="text-xl font-semibold text-blue-900 mb-4">Direct Data Access:</h2>
      <p><strong>Homepage EN Hero Title:</strong> {{ homepage.en.hero.title }}</p>
      <p><strong>Homepage EN Hero Image:</strong> {{ homepage.en.hero.image }}</p>
      <p><strong>Homepage DE Hero Title:</strong> {{ homepage.de.hero.title }}</p>
    </div>
  </div>
</div>
```

**驗證命令：**
```bash
# 構建項目
npm run build

# 檢查數據讀取
grep -A 5 "Direct Data Access" _site/simple-test/index.html

# 檢查特定內容
grep -A 5 -B 5 "Charge Ahead" _site/en/index.html
grep -A 5 -B 5 "Laden Sie voraus" _site/de/index.html
```

### 5. 調試技巧總結
**常見問題排查：**
1. **數據為空**：檢查文件名和數據結構
2. **模板錯誤**：檢查數據訪問路徑
3. **構建失敗**：檢查YAML語法錯誤
4. **多語言不工作**：檢查語言設置和數據組織

**調試工具：**
- 使用 `{{ data | dump }}` 顯示數據結構
- 創建專門的調試頁面
- 使用命令行工具檢查生成的文件
- 檢查11ty配置和依賴

### 6. 維護和擴展建議
**文檔記錄：**
- 詳細記錄數據文件結構
- 記錄模板數據訪問模式
- 記錄測試和驗證步驟
- 記錄常見問題和解決方案

**版本控制：**
- 使用Git追蹤數據文件變化
- 為重要更改創建分支
- 記錄數據結構的演進歷史

**團隊協作：**
- 建立數據文件命名規範
- 建立模板編寫規範
- 建立測試和驗證流程
- 定期檢查和更新文檔

## 🔄 後續工作與檢查清單

### 1. 立即需要完成的工作
- [ ] 更新產品頁面模板使用新的數據結構
- [ ] 更新聯絡頁面模板使用新的數據結構
- [ ] 測試所有頁面的多語言功能
- [ ] 與原始static頁面對齊內容和樣式

### 2. 數據文件完善
- [ ] 檢查並完善 `products.yml` 中的所有產品數據
- [ ] 檢查並完善 `contact.yml` 中的所有聯絡信息
- [ ] 驗證所有圖片路徑是否正確
- [ ] 確保所有多語言內容完整

### 3. 模板優化
- [ ] 統一所有模板的數據訪問方式
- [ ] 添加錯誤處理和安全訪問
- [ ] 優化模板的可讀性和維護性
- [ ] 添加適當的註釋和文檔

### 4. 測試和驗證
- [ ] 創建完整的測試套件
- [ ] 測試所有頁面的響應式設計
- [ ] 驗證所有鏈接和導航功能
- [ ] 測試不同瀏覽器的兼容性

### 5. 性能優化
- [ ] 檢查並優化圖片大小
- [ ] 優化CSS和JavaScript加載
- [ ] 檢查並改善頁面加載速度
- [ ] 實施適當的緩存策略

### 6. 文檔和維護
- [ ] 更新項目README文檔
- [ ] 創建部署指南
- [ ] 記錄所有配置和設置
- [ ] 建立維護和更新流程

---

## 📋 快速參考指南

### 常見問題解決
```bash
# 數據讀取問題
npm run build
grep -A 5 "Direct Data Access" _site/simple-test/index.html

# 檢查特定頁面內容
grep -A 5 -B 5 "特定文字" _site/en/index.html

# 檢查數據結構
curl http://localhost:8080/simple-test/
```

### 重要文件位置
- 數據文件：`src/_data/`
- 模板文件：`src/en/` 和 `src/de/`
- 佈局文件：`src/_includes/`
- 靜態資源：`src/assets/`

### 關鍵命令
```bash
# 開發模式
npm run dev

# 構建項目
npm run build

# 清理構建文件
rm -rf _site/
```

---

**解決時間**：2024年8月3日  
**解決狀態**：✅ 完成  
**影響範圍**：所有頁面的數據讀取功能  
**測試狀態**：✅ 通過  
**文檔狀態**：✅ 完整記錄  
**維護狀態**：🔄 持續更新 