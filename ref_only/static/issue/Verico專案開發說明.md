# ✅ Verico 轉換為 11ty 無頭 CMS 完整指南（含多語言）

本指南將原始的 4 個 HTML 頁面轉換為模組化、可維護的 11ty 無頭 CMS 架構，支援多語言，採用：

* Tailwind CSS
* Nunjucks 模板
* YAML 資料組織
* `i18n` 國際化資料夾

---

## 🗂 靜態頁面對應

| 檔名                     | 功能說明                 | 對應模板                                                | 對應資料檔案               |
| ---------------------- | -------------------- | --------------------------------------------------- | -------------------- |
| `index.html`           | 首頁（Hero + 分類 + 熱門產品） | `en/index.njk` / `de/index.njk`                     | `homepage.yml`       |
| `product-catalog.html` | 產品分類總覽頁面             | `en/product-catalog.njk` / `de/product-catalog.njk` | `products.yml`       |
| `product-spec.html`    | 單一產品詳細頁（含圖文與規格）      | `products/{slug}/index.njk`                         | `product-{slug}.yml` |
| `contact.html`         | 聯絡頁（含表單與常見問答）        | `en/contact.njk` / `de/contact.njk`                 | `contact.yml`        |

---

## 🏠 一、專案結構規範（含多語言）

```bash
src/
  ├── en/              # English page content
  │    ├── index.njk
  │    ├── product-catalog.njk
  │    ├── contact.njk
  │    └── products/{slug}/index.njk
  ├── de/              # German (Deutsch) content
  │    └── ... (與 en 同結構)
  ├── _data/
  │    ├── site.yml              # 靜態資訊（logo、品牌標語）
  │    ├── navigation.yml        # 多語選單（含 i18n title）
  │    ├── homepage.yml          # 首頁資料，包含 en/de
  │    ├── products.yml          # 所有產品分類與列表資料，包含 en/de
  │    ├── contact.yml           # 聯絡資料與 FAQ，包含 en/de
  │    ├── product-{slug}.yml    # 每個產品詳細資訊，支援多語（可依需求）
  ├── _includes/
  │    ├── layout.njk            # 主框架，引用 nav/footer/head 樣板
  │    ├── nav.njk               # 導覽列（含語言切換器）
  │    ├── footer.njk            # 頁尾
  │    └── head.njk              # <head> 區塊共用模板（meta、fonts、css）
  ├── assets/
  │    ├── css/                  # Tailwind CSS 相關自訂樣式（可選）
  │    └── js/                   # 前端互動腳本，如語言切換、下拉選單
```

⚠️ YAML 多語命名建議統一寫法為 `homepage.yml` → `homepage.en.title`, `homepage.de.title` 這種格式，不再使用 `index.en.yml` 等點號語言後綴方式，以避免 Eleventy 輸出解析錯誤。

---

## 🌐 二、多語言支援要點

### 1. 資料組織結構

* 使用單一 YAML 檔（如 `homepage.yml`）儲存所有語言版本：

```yaml
# homepage.yml
en:
  hero:
    title: "Charge Ahead.<br>Store Smart."
    image: "assets/images/hero.jpg"
    alt: "Hero Banner"

de:
  hero:
    title: "Laden Sie voraus.<br>Speichern Sie intelligent."
    image: "assets/images/hero.jpg"
    alt: "Hero Banner"
```

* `products.yml`, `contact.yml` 同理。

### 2. 模板使用 `lang` 動態語言切換

在 `.njk` 模板內應這樣引用：

```njk
{% set data = homepage[lang] %}
<h1>{{ data.hero.title }}</h1>
```

`lang` 通常從 front matter 中指定，例如：

```njk
---
layout: layout.njk
title: Home
lang: en
permalink: /en/
---
```

### 3. 導覽選單與 footer 多語支援

`navigation.yml` 結構建議如下：

```yaml
en:
  main:
    - title: Home
      url: /en/
    - title: Products
      url: /en/product-catalog
    - title: Contact
      url: /en/contact
de:
  main:
    - title: Startseite
      url: /de/
    - title: Produkte
      url: /de/product-catalog
    - title: Kontakt
      url: /de/contact
```

在 `nav.njk` 中可引用：

```njk
{% for item in navigation[lang].main %}
  <a href="{{ item.url }}">{{ item.title }}</a>
{% endfor %}
```

### 4. 多語切換器元件（建議做法）

```njk
<div class="language-switcher">
  <a href="/en/{{ page.fileSlug }}/">EN</a> |
  <a href="/de/{{ page.fileSlug }}/">DE</a>
</div>
```

（可加入 JS 自動判斷瀏覽器語系做 redirect）

---

## 🐛 YAML 數據讀取問題說明

### 問題概述

早期資料命名如 `index.en.yml`、`products.en.yml` 導致 11ty 在讀取資料時產生命名衝突，結果導致：

* `{% set data = index.en %}` 會找不到 `en`
* `{{ index.en.hero.title }}` 無法讀取正確資料

### 原因解析

11ty 將 `index.en.yml` 認定為變數 `index`，但 `index` 不是物件，語法錯誤。

```yaml
# 錯誤命名
src/_data/index.en.yml → index: {...}（11ty 認定為 index）
```

### 正確做法

使用單一檔案包含多語系內容：

```yaml
# 正確命名：homepage.yml
en:
  hero:
    title: "..."
    image: "..."
de:
  hero:
    title: "..."
    image: "..."
```

### 模板內正確使用方式

```njk
{% set data = homepage[lang] %}
<h1>{{ data.hero.title }}</h1>
```

### 建議結構調整步驟：

1. 移除所有 `index.en.yml`, `products.en.yml` 等錯誤命名格式
2. 將所有語系資料統一寫入：`homepage.yml`, `products.yml`, `contact.yml`
3. 使用 `{% set data = homepage[lang] %}` 為資料起始點
4. 若需除錯，加上：`{{ homepage | dump }}`

### 建議測試頁（debug page）

```njk
---
layout: layout.njk
title: Debug Page
lang: en
permalink: /debug/
---
<pre>{{ homepage | dump }}</pre>
<pre>{{ products | dump }}</pre>
<pre>{{ contact | dump }}</pre>
```

✅ 修正後，可成功讀取多語言內容並動態生成對應區塊。
