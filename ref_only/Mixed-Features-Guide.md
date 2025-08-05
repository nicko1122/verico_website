# 混合配圖使用指南

## 基本概念

在產品 Markdown 文件中，你可以混合使用有圖片和沒有圖片的特點：

### 有圖片的特點
```markdown
<!-- FEATURE:feature-1.jpg -->
- **High Capacity:** 2550mWh / 1700mAh (at 1.5V) for extended device usage.
```

### 沒有圖片的特點
```markdown
- **Long Cycle Life:** Rechargeable over 1000 times, saving thousands of alkaline batteries.
```

## 完整示例

```markdown
# 產品名稱

<!-- IMAGES: main.jpg -->
<!-- GALLERY: Product-1.png, Product-2.png, Product-3.png, Product-4.png -->

產品介紹...

## Key Features

<!-- FEATURE:feature-1.jpg -->
- **High Capacity:** 2550mWh / 1700mAh (at 1.5V) for extended device usage.

<!-- FEATURE:feature-2.jpg -->
- **Fast USB Type-C Charging:** Fully charges in 1-2 hours with universal compatibility.

- **Long Cycle Life:** Rechargeable over 1000 times, saving thousands of alkaline batteries.

<!-- FEATURE:feature-4.jpg -->
- **LED Charge Indicator:** Intelligent power indicator for real-time charging status.

- **Advanced Safety Protections:** Multiple safeguards against over-charge, over-discharge, overheating, and short circuit.

<!-- FEATURE:feature-6.jpg -->
- **Patented Integrated PCB Design:** Ensures stable performance and safety.

- **Eco-Friendly:** Reduces landfill waste and environmental footprint.
```

## 系統處理方式

### 有圖片的特點
- ✅ 會使用指定的圖片
- ✅ 在 YAML 中會包含圖片路徑
- ✅ 在網站上會顯示圖片

### 沒有圖片的特點
- ✅ 會使用預設圖標（如 lightning, shield, check 等）
- ✅ 在 YAML 中不會包含圖片路徑
- ✅ 在網站上會顯示圖標

## 生成的 YAML 結構

```yaml
features:
  - title: "High Capacity"
    description: "2550mWh / 1700mAh (at 1.5V) for extended device usage"
    icon: "lightning"
    image: "/assets/images/product/product-name/feature-1.jpg"
    
  - title: "Fast USB Type-C Charging"
    description: "Fully charges in 1-2 hours with universal compatibility"
    icon: "lightning"
    image: "/assets/images/product/product-name/feature-2.jpg"
    
  - title: "Long Cycle Life"
    description: "Rechargeable over 1000 times, saving thousands of alkaline batteries"
    icon: "shield"
    # 沒有 image 字段
    
  - title: "LED Charge Indicator"
    description: "Intelligent power indicator for real-time charging status"
    icon: "lightning"
    image: "/assets/images/product/product-name/feature-4.jpg"
```

## 建議

1. **重要特點配圖** - 為最重要的特點配圖
2. **次要特點用圖標** - 次要特點可以使用圖標
3. **保持一致性** - 同類型的特點使用相同的配圖方式
4. **靈活搭配** - 根據需要靈活選擇是否配圖 