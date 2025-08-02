# Verico 轉換為 11ty 無頭 CMS 完整指南

本指南用於將 Verico 現有的 4 個 HTML 頁面整合為 11ty (十一字)基礎框架的無頭 CMS 綱要格式，依照背景用 Tailwind CSS、弄網站組件化、以 YAML 為資料主體。

---

## 一、全局組織

### 公用模板

* `/_includes/layout.njk` 作為公用 layout
* `/_includes/nav.njk` 展示主頁和交流對應路徑
* `/_includes/footer.njk`
* 預設 `base.njk` 為所有 page 引用 layout

### 格式 / JS

* Tailwind CSS CDN 保留在 layout
* JS 用 `/js/*.js` 存放，使用 `<script src="...">` 引入
* 【註】原本所有頁面的「強制刷新」script 為開發期間管理為主，在 11ty 中已不需要，可以全部刪除

---

## 二、資料源 YAML 模組

### `/_data/site.yml`

```yaml
title: Verico
tagline: We care & We share
description: We care & We share
```

### `/_data/navigation.yml`

```yaml
main:
  - title: Home
    url: /
  - title: Products
    url: /products
    submenu:
      - title: Powerbank
        url: /products/powerbank
        submenu:
          - title: Power Pro
            url: /products/powerbank/powerpro
          - title: Power PD
            url: /products/powerbank/powerpd
      - title: Loopenergy
        url: /products/loopenergy
      - title: GaN Charger
        url: /products/gan-charger
      - title: Flash Disk
        url: /products/flash-disk
  - title: Contact
    url: /contact
```

---

## 三、個別頁面轉換

### `index.html` 轉換 `index.njk`

* Hero Section 變成 `/_data/index.yml`

```yaml
hero:
  image: assets/images/banner/hero/Carousel/GaNCharger-banner.jpg
  title: Charge Ahead.<br>Store Smart.
```

* Category Grid

```yaml
categories:
  - name: Power Pro Series
    image: assets/images/banner/tab/product-tab/powerbank-tab.png
    text: High Capacity. Fast Charge.
```

* Trending Products Block Grid

```yaml
trending_products:
  - name: MOJO 140W GaN Charger
    image: assets/images/product/Gan_140W/product-1.jpg
    desc1: Ultra-fast charging with GaN.
    desc2: Perfect for laptops.
```

### `products.html` 轉換 `products.njk`

* `/_data/products.yml`

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
      ...
```

### `product-spec.html` 用合模組 + 預設 route

* `products/{slug}/index.njk`
* 資料使 `/products/{slug}.yml`

```yaml
title: MOJO 140W GaN Charger
series: Premium Series
description: Experience ultra-fast charging...
images:
  - assets/images/product/Gan_140W/mojo-140w-gan-1.png
features:
  - title: GaN Technology
    description: ...
    bullets: [...]
    image: ...
specs:
  - key: Output Power
    value: 140W Max
compatibility:
  - title: Smartphones
    note: iPhone, Samsung...
package:
  - name: Charger
    desc: GaN Charger body
```

### `contact.html`

* `contact.njk`
* FAQ + contact info 資料來自 `/_data/contact.yml`
* 表單可保留手動作，後續可以上传到網路服務 (e.g. Netlify Forms)

---

## 四、開發項目設定

1. 所有 page 都使用 `layout.njk`
2. `eleventyComputed` 來用 slug 生成路徑 `/products/:slug/`
3. 所有 block, product card 以 Nunjucks loop 輸出
4. `/assets/`, `/js/`, `/images/` 不加處理

---

如需我可提供 YAML 組織草稿與 Nunjucks 範例模板編写
