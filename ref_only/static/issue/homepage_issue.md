# Homepage 數據分離與語言跳轉解決方案

## 🎯 問題背景

在 Eleventy 靜態網站生成器中，我們遇到了 homepage 數據管理的問題：

### 原始問題
1. **數據重複**：同時存在 `homepage.yml`、`homepage.en.yml`、`homepage.de.yml` 三個文件
2. **模板讀取問題**：模板使用 `{% set data = homepage.en %}` 需要合併的數據結構
3. **維護困難**：合併文件導致英文和德文數據難以獨立維護

### 用戶需求
- 分離英文和德文數據文件，便於獨立維護
- 實現智能語言檢測和跳轉
- 使用 Cookie 記住用戶語言偏好

## 🛠️ 解決方案

### 1. 數據文件結構重組

#### 刪除合併文件
```bash
# 刪除合併的 homepage.yml
rm src/_data/homepage.yml
```

#### 保留分離文件
```
src/_data/
├── homepage.en.yml    # 英文數據 (載入為 homepageen)
└── homepage.de.yml    # 德文數據 (載入為 homepagede)
```

### 2. 模板數據引用修改

#### 英文模板 (`src/en/index.njk`)
```diff
- {% set data = homepage.en %}
+ {% set data = homepageen %}
```

#### 德文模板 (`src/de/index.njk`)
```diff
- {% set data = homepage.de %}
+ {% set data = homepagede %}
```

### 3. 智能跳轉頁面

創建 `src/index.njk` 作為根目錄跳轉頁面：

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
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .loader {
            text-align: center;
        }
        .spinner {
            border: 3px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top: 3px solid white;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
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

### 4. 語言切換組件

創建 `src/_includes/language-switcher.njk`：

```html
<!-- Language Switcher Component -->
<div class="language-switcher fixed top-4 right-4 z-50">
    <div class="relative">
        <button id="langToggle" class="bg-white border border-gray-200 rounded-lg px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors flex items-center gap-2">
            <span id="currentLang">EN</span>
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
            </svg>
        </button>
        <div id="langDropdown" class="absolute right-0 mt-2 w-32 bg-white border border-gray-200 rounded-lg shadow-lg opacity-0 invisible transition-all duration-200">
            <a href="/en/" class="block px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors" data-lang="en">English</a>
            <a href="/de/" class="block px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors" data-lang="de">Deutsch</a>
        </div>
    </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const langToggle = document.getElementById('langToggle');
    const langDropdown = document.getElementById('langDropdown');
    const currentLang = document.getElementById('currentLang');
    
    // 設置當前語言顯示
    const path = window.location.pathname;
    if (path.startsWith('/de/')) {
        currentLang.textContent = 'DE';
    } else {
        currentLang.textContent = 'EN';
    }
    
    // 切換下拉菜單
    langToggle.addEventListener('click', function() {
        const isVisible = langDropdown.classList.contains('opacity-100');
        if (isVisible) {
            langDropdown.classList.remove('opacity-100', 'visible');
            langDropdown.classList.add('opacity-0', 'invisible');
        } else {
            langDropdown.classList.remove('opacity-0', 'invisible');
            langDropdown.classList.add('opacity-100', 'visible');
        }
    });
    
    // 點擊外部關閉下拉菜單
    document.addEventListener('click', function(event) {
        if (!langToggle.contains(event.target) && !langDropdown.contains(event.target)) {
            langDropdown.classList.remove('opacity-100', 'visible');
            langDropdown.classList.add('opacity-0', 'invisible');
        }
    });
    
    // 語言切換處理
    langDropdown.addEventListener('click', function(event) {
        if (event.target.tagName === 'A') {
            const lang = event.target.getAttribute('data-lang');
            
            // 設置 cookie
            const expiryDate = new Date();
            expiryDate.setDate(expiryDate.getDate() + 30);
            document.cookie = `preferred_language=${lang}; expires=${expiryDate.toUTCString()}; path=/`;
        }
    });
});
</script>
```

### 5. 布局文件更新

在 `src/_includes/layout.njk` 中添加語言切換器：

```diff
  <body class="bg-white text-gray-900">
+   <!-- Language Switcher -->
+   {% include "language-switcher.njk" %}
+   
    <!-- Navigation -->
    {% include "nav.njk" %}
```

## 🎯 工作流程

### 首次訪問
1. 用戶訪問 `http://localhost:8080/`
2. 系統檢測用戶地區/瀏覽器語言
3. 自動跳轉到 `/en/` 或 `/de/`
4. 設置 `preferred_language` cookie

### 後續訪問
1. 檢查 cookie 中的語言偏好
2. 直接跳轉到相應語言版本

### 手動切換
1. 右上角的語言切換器
2. 點擊可切換語言並更新 cookie

## ✅ 解決的問題

1. **✅ 數據分離** - 英文和德文數據完全獨立，易於維護
2. **✅ 智能檢測** - 自動根據地區選擇語言
3. **✅ 用戶控制** - 可以手動切換語言
4. **✅ Cookie 記憶** - 記住用戶偏好
5. **✅ 無重複數據** - 避免了數據重複和同步問題

## 📁 最終文件結構

```
src/
├── _data/
│   ├── homepage.en.yml    # 英文數據
│   └── homepage.de.yml    # 德文數據
├── _includes/
│   ├── layout.njk         # 主布局
│   └── language-switcher.njk  # 語言切換器
├── en/
│   └── index.njk          # 英文首頁 (使用 homepageen)
├── de/
│   └── index.njk          # 德文首頁 (使用 homepagede)
└── index.njk              # 跳轉頁面
```

## 🔧 技術細節

### Eleventy 數據載入規則
- `homepage.en.yml` → 載入為 `homepageen`
- `homepage.de.yml` → 載入為 `homepagede`
- 模板中使用 `{% set data = homepageen %}` 或 `{% set data = homepagede %}`

### Cookie 設置
- 名稱：`preferred_language`
- 值：`en` 或 `de`
- 過期時間：30天
- 路徑：`/`

### 語言檢測邏輯
1. 優先檢查 cookie
2. 檢查瀏覽器語言設置
3. 檢測德語國家代碼 (de, at, ch, li, lu)
4. 默認使用英文

這個解決方案完美解決了數據分離和模板讀取的問題，同時提供了良好的用戶體驗！ 