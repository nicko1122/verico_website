# 範例產品包

這是一個範例產品包，展示如何準備產品數據。

## 文件結構

```
example-product.zip
├── spec.md              # 產品規格文本
├── images/              # 產品圖片
│   ├── product-1.jpg
│   ├── product-2.jpg
│   └── feature-1.jpg
└── metadata.json        # 額外信息（可選）
```

## 創建產品包的步驟

1. **準備產品文本** (`spec.md`)
   - 包含產品名稱、描述、特色
   - 添加技術規格表格
   - 使用清晰的格式

2. **準備圖片** (`images/`)
   - 主產品圖片：`product-1.jpg`, `product-2.jpg`
   - 特色圖片：`feature-1.jpg`
   - 建議尺寸：600x600px（主圖），400x200px（特色圖）

3. **打包文件**
   - 將所有文件放入一個目錄
   - 壓縮為 ZIP 文件
   - 使用 kebab-case 命名

4. **放入監控目錄**
   - 將 ZIP 文件放入 `product-packages/`
   - 系統會自動檢測並處理

## 範例產品文本

```markdown
Thunder SSD Pro
Ultimate Speed, Maximum Performance
Experience lightning-fast storage with the Thunder SSD Pro, designed for professionals who demand the best.

Lightning Speed
Read speeds up to 3500MB/s for instant file access and system boot times.

Advanced Technology
Built with the latest NVMe 3.0 technology and 3D NAND flash memory.

Multiple Capacities
Available in 256GB, 512GB, 1TB, and 2TB capacities to suit your needs.

Specifications
Capacity    256GB    512GB    1TB    2TB
Interface   PCIe 4.0 x4, NVMe 2.0
Read Speed  3200MB/s  3400MB/s  3500MB/s  3500MB/s
Write Speed 1200MB/s  2400MB/s  3200MB/s  3000MB/s
Warranty    5 Years
```

## 注意事項

- 確保文本格式清晰易讀
- 包含完整的技術規格
- 圖片質量要高
- 文件名使用英文和數字
- ZIP 文件大小建議不超過 10MB 