# 圖片路徑問題解決記錄

## 問題描述
網站中的圖片無法正常顯示，在瀏覽器中檢查發現圖片路徑缺少前導斜線 `/`，導致路徑解析錯誤。

### 原始問題
- 生成的 HTML 中圖片路徑為：`src="assets/images/..."`
- 正確的路徑應該是：`src="/assets/images/..."`

## 解決過程

### 1. 初步診斷
首先檢查了生成的 HTML 文件，發現圖片路徑缺少前導斜線：
```bash
grep -A 2 -B 2 "GaNCharger-banner" _site/en/index.html
```
結果顯示：
```html
<img src="assets/images/banner/hero/Carousel/GaNCharger-banner.jpg" alt="Verico Hero Banner"
```

### 2. 檢查數據文件
檢查了 `src/_data/homepage.en.yml` 文件，發現圖片路徑已經有前導斜線：
```yaml
hero:
  title: "Charge Ahead.\nStore Smart."
  image: "/assets/images/banner/hero/Carousel/GaNCharger-banner.jpg"
  alt: "Verico Hero Banner"
```

### 3. 發現根本問題
發現存在多個數據文件，其中 `src/_data/homepage.yml` 文件中的圖片路徑沒有前導斜線，這個文件可能優先於 `homepage.en.yml`。

### 4. 修正所有相關文件

#### 4.1 修正 `src/_data/homepage.yml`
將所有圖片路徑添加前導斜線：

**Hero 區塊：**
```yaml
en:
  hero:
    title: "Charge Ahead.\nStore Smart."
    image: "/assets/images/banner/hero/Carousel/GaNCharger-banner.jpg"  # 添加 /
    alt: "Verico Hero Banner"
```

**產品分類區塊：**
```yaml
categories:
  - name: "Power Pro Series"
    description: "High Capacity. Fast Charge. Endless Energy."
    image: "/assets/images/banner/tab/product-tab/powerbank-tab.png"  # 添加 /
    link: "/en/products/powerbank"
  - name: "Loopenergy Series"
    description: "Smart Power. Eco Friendly. Built to Last."
    image: "/assets/images/banner/tab/product-tab/loopenergy-tab.png"  # 添加 /
    link: "/en/products/loopenergy"
  - name: "GaN MOJO Series"
    description: "Ultra Fast. Ultra Safe. Ultra Storage."
    image: "/assets/images/banner/tab/product-tab/gancharger-tab.png"  # 添加 /
    link: "/en/products/gan-charger"
  - name: "Memory Series"
    description: "Ultra Fast. Ultra Safe. Ultra Storage."
    image: "/assets/images/banner/tab/product-tab/usb-tab.png"  # 添加 /
    link: "/en/products/flash-disk"
```

**熱門產品區塊：**
```yaml
trending_products:
  products:
    - name: "MOJO 140W GaN Charger"
      image: "/assets/images/product/Gan_140W/product-1.jpg"  # 添加 /
    - name: "Power Pro 10000mAh"
      image: "/assets/images/product/Gan_65W/product-1.jpg"  # 添加 /
    - name: "Loopenergy 10000mAh"
      image: "/assets/images/product/loop_AAA/product-1.jpg"  # 添加 /
    - name: "MOJO 65W GaN Charger"
      image: "/assets/images/product/Loop_AA/product-1.jpg"  # 添加 /
    - name: "USB 3.0 64GB"
      image: "/assets/images/product/Loop_C/product-1.jpg"  # 添加 /
    - name: "USB 3.0 128GB"
      image: "/assets/images/product/Loop_PP3/product-1.jpg"  # 添加 /
```

**關於區塊：**
```yaml
about:
  logo: "/assets/images/verico-logo-white.svg"  # 添加 /
```

### 5. 驗證修復
重新生成網站並檢查生成的 HTML：
```bash
grep -A 2 -B 2 "GaNCharger-banner" _site/en/index.html
```

結果顯示路徑已正確：
```html
<img src="/assets/images/banner/hero/Carousel/GaNCharger-banner.jpg" alt="Verico Hero Banner"
```

## 技術要點

### 1. 路徑類型
- **相對路徑**：`assets/images/...` - 相對於當前頁面路徑
- **絕對路徑**：`/assets/images/...` - 相對於網站根目錄

### 2. 11ty 數據文件優先級
在 11ty 中，數據文件的載入順序可能影響最終結果。需要確保所有相關的數據文件都有一致的路徑格式。

### 3. 文件結構
```
src/_data/
├── homepage.yml          # 主要數據文件（包含 en 和 de）
├── homepage.en.yml       # 英文專用數據文件
└── homepage.de.yml       # 德文專用數據文件
```

## 預防措施

1. **統一路徑格式**：所有圖片路徑都使用絕對路徑（以 `/` 開頭）
2. **檢查所有數據文件**：確保所有相關的 YAML 文件都有一致的路徑格式
3. **測試驗證**：每次修改後都要檢查生成的 HTML 文件

## 總結
通過系統性地檢查和修正所有相關的數據文件，成功解決了圖片路徑問題。關鍵是要確保所有數據文件中的圖片路徑都使用正確的絕對路徑格式。 