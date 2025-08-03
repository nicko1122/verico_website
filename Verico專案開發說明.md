# ✅ Verico 轉換為 11ty 無頭 CMS 完整指南（含多語言）

本指南將原始的 4 個 HTML 頁面轉換為模組化、可維護的 11ty 無頭 CMS 架構，支援多語言，採用：

* Tailwind CSS
* Nunjucks 模板
* YAML 資料組織
* `i18n` 國際化資料夾

---

## 🗂 靜態頁面對應
"/home/nicko1122/webproject/verico/static"
| 檔名                     | 功能說明                 |
| ---------------------- | -------------------- |
| `index.html`           | 首頁（Hero + 分類 + 熱門產品） |
| `product-catalog.html` | 產品分類總覽頁面             |
| `product-spec.html`    | 單一產品詳細頁（含圖文與規格）      |
| `contact.html`         | 聯絡頁（含表單與常見問答）        |

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
  │    ├── index.{lang}.yml      # 首頁 Hero + 區塊
  │    ├── products.{lang}.yml   # 產品類別與簡略資料
  │    ├── product-[slug].{lang}.yml # 單一產品詳細資料
  │    └── contact.{lang}.yml    # 聯繫方式、FAQ
  ├── _includes/
  │    ├── layout.njk            # 主框架，引用 nav/footer/head 樣板
  │    ├── nav.njk               # 導覽列（含語言切換器）
  │    ├── footer.njk            # 頁尾
  │    └── head.njk              # <head> 區塊共用模板（meta、fonts、css）
  ├── assets/
  │    ├── css/                  # Tailwind CSS 相關自訂樣式（可選）
  │    └── js/                   # 前端互動腳本，如語言切換、下拉選單
```

---

## 🌐 二、多語言支援要點

### 1. 多語言分頁

每語系對應資料夾（`en/`, `de/`）
→ 使用 `permalink: /{{ lang }}/products/` 控制輸出路徑。

### 2. YAML 命名規則

```yaml
# index.en.yml
hero:
  image: assets/images/banner/hero/Carousel/GaNCharger-banner.jpg
  title: Charge Ahead.<br>Store Smart.

categories:
  - name: Power Pro Series
    image: assets/images/banner/tab/product-tab/powerbank-tab.png
    text: High Capacity. Fast Charge.
```

---

## 📂 三、導航選單 (多語言)

```yaml
# navigation.yml
main:
  - title:
      en: Home
      de: Startseite
    url: /
  - title:
      en: Products
      de: Produkte
    url: /products/
    submenu:
      - title:
          en: Powerbank
          de: Powerbank
        url: /products/powerbank
        submenu:
          - title:
              en: Power Pro
              de: Power Pro
            url: /products/powerbank/powerpro
          - title:
              en: Power PD
              de: Power PD
            url: /products/powerbank/powerpd
```

在 `nav.njk` 中，根據 `page.lang` 選擇語系：

```njk
{% set t = nav.title[lang] or nav.title['en'] %}
```

> 語言切換器建議搭配 dropdown + `lang` 資料夾路徑自動切換（如 `/en/...` ↔ `/de/...`）。

---

## 🧩 四、頁面資料（多語）

### ✅ `index.{lang}.yml`

```yaml
hero:
  image: assets/images/banner/hero/Carousel/GaNCharger-banner.jpg
  title: Charge Ahead.<br>Store Smart.

categories:
  - name: Power Pro Series
    image: assets/images/banner/tab/product-tab/powerbank-tab.png
    text: High Capacity. Fast Charge.

trending_products:
  - name: MOJO 140W GaN Charger
    image: assets/images/product/Gan_140W/product-1.jpg
    desc1: Ultra-fast charging with GaN.
    desc2: Perfect for laptops.
```

### ✅ `products.{lang}.yml`

```yaml
categories:
  - id: powerbank
    label: Powerbank Series
    products:
      - name: Power Pro 10000mAh
        image: assets/images/product/Gan_65W/product-1.jpg
        short: High-capacity fast charger
        long: Reliable power for your devices
  - id: loopenergy
    label: Loopenergy Series
    products:
      - name: Loopenergy 10000mAh
        image: assets/images/product/Loop_AA/product-1.jpg
        short: Eco-friendly compact charger
        long: Made for sustainable performance
```

### ✅ `product-[slug].{lang}.yml`

```yaml
title: MOJO 140W GaN Charger
series: Premium Series
description: Experience ultra-fast charging...
images:
  - assets/images/product/Gan_140W/mojo-140w-gan-1.png
  - assets/images/product/Gan_140W/mojo-140w-gan-2.png
features:
  - title: GaN Technology
    description: Efficient power conversion
    bullets:
      - 50% smaller
      - 30% more efficient
      - Less heat
    image: assets/images/product/features/gan-technology-comparison.jpg
specs:
  - key: Output Power
    value: 140W Max
  - key: USB-C Ports
    value: 2x USB-C
compatibility:
  - title: Smartphones
    note: iPhone, Samsung...
package:
  - name: Charger
    desc: GaN Charger body
  - name: USB-C Cable
    desc: 100W PD charging cable
```

### ✅ `contact.{lang}.yml`

```yaml
hero_title: Contact Us
hero_desc: Reach out for professional solutions.

contact:
  phone: +886 2 2345 6789
  email: info@verico.com
  address: No. 123, Tech Street, Taipei

faq:
  - q: Do you ship internationally?
    a: Yes, worldwide shipping is available.
  - q: What payment methods are supported?
    a: Credit card, PayPal, and wire transfer.
```

---

## ⚙️ 五、模組化資源（CSS、JS、模板）

### ✅ CSS

* 主要以 CDN tailwind 為主，也可使用 `assets/css/main.css` 自定義（需設定 PostCSS 或 Tailwind CLI）。
* 建議 Tailwind 的 `config` 設定獨立 `tailwind.config.js`

### ✅ JS

* 模組化放入 `assets/js/*.js`
* 常見功能：語言切換器、產品分類切換、下拉選單、圖片輪播等
* 在 `layout.njk` 統一引入：

```html
<script src="/assets/js/lang-toggle.js"></script>
```

### ✅ 模板共用區塊（Nunjucks）

| 模板檔案               | 功能                      |
| ------------------ | ----------------------- |
| `layout.njk`       | 包含頁框、head、nav、footer    |
| `nav.njk`          | 主導覽列，含 submenu 支援       |
| `footer.njk`       | 公司資訊與版權                 |
| `head.njk`         | 共用 <head>，meta/font/css |
| `product-card.njk` | 可選：商品卡元件片段              |

---

## ✅ 小結

| 元件           | 多語 YAML | Nunjucks 調整        |
| ------------ | ------- | ------------------ |
| nav/footer   | ✅       | 用 `lang` 指定 key    |
| 首頁 hero      | ✅       | 動態圖片與標語            |
| Product grid | ✅       | 用 `loop` 自動 render |
| FAQ / 聯絡     | ✅       | 問答與公司資訊資料分離        |
| 模板結構         | ✅       | 模組化 partial 共用     |
| JS / CSS     | ✅       | 模組化資源統一引入          |

---

