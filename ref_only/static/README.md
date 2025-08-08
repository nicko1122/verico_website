# 靜態開發環境

這個目錄用於靜態頁面開發，完成後再轉換成 11ty 模板。

## 目錄結構

```
static/
├── index.html          # 首頁
├── pages/              # 其他頁面
├── components/          # 可重用的組件
└── assets/
    ├── css/            # 樣式檔案
    ├── js/             # JavaScript 檔案
    └── images/         # 圖片檔案
```

## 開發指令

### 啟動靜態伺服器
```bash
npm run static
```
或
```bash
cd static && python3 -m http.server 3000
```

### 存取網頁
- 首頁：http://localhost:3000/index.html
- 或直接：http://localhost:3000/

## 開發流程

1. **靜態開發階段**：
   - 在 `static/` 目錄下開發所有頁面
   - 使用 `npm run static` 啟動伺服器
   - 完成所有頁面設計和功能

2. **轉換階段**：
   - 將完成的 HTML 檔案轉換成 11ty 模板
   - 移動到 `src/` 目錄
   - 設定 11ty 配置

## 注意事項

- 所有資源路徑都使用相對路徑
- 圖片路徑：`assets/images/`
- CSS 路徑：`assets/css/`
- JS 路徑：`assets/js/` 