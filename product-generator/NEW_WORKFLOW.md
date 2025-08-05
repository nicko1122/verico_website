# 新的分段工作流程

## 🎯 目標
將複雜的產品處理流程分解為多個獨立步驟，便於調試和維護。

## 📋 工作流程

### 階段 1: 文件處理
```bash
python step1_extract.py
```
**功能:**
- 解包 ZIP 文件
- 移動圖片到正確位置
- 讀取 spec.md 文件
- 保存中間數據到 `step1_data_[product].json`

### 階段 2: LLM 處理
```bash
python step2_llm.py
```
**功能:**
- 載入第一階段數據
- 創建標準化模板給 LLM
- 生成英文 YAML
- 生成德文 YAML
- 保存到 `src/_data/content/products/details/[product]/`

### 階段 3: 頁面生成 (待實現)
```bash
python step3_pages.py
```
**功能:**
- 生成頁面文件
- 自動更新 Eleventy 配置
- 重新構建網站

## 🔧 使用方法

### 手動處理
1. 將產品包放入 `product-packages/`
2. 運行階段 1: `python step1_extract.py`
3. 檢查結果，如有問題可重複運行
4. 運行階段 2: `python step2_llm.py`
5. 檢查生成的 YAML 文件
6. 運行階段 3: `python step3_pages.py`

### 自動處理 (可選)
```bash
python process_all.py
```
一次性運行所有階段

## ✅ 優點

1. **錯誤隔離** - 每個階段獨立，出錯時容易定位
2. **可重複執行** - 可以單獨重新運行某個階段
3. **易於調試** - 每個階段都有明確的輸入輸出
4. **靈活性** - 可以手動檢查和修改中間結果
5. **可維護性** - 每個腳本職責單一，易於修改

## 📁 文件結構

```
product-generator/
├── step1_extract.py      # 階段 1: 文件處理
├── step2_llm.py         # 階段 2: LLM 處理
├── step3_pages.py       # 階段 3: 頁面生成 (待實現)
├── process_all.py       # 自動處理所有階段
├── step1_data_*.json    # 第一階段中間數據
└── config.json          # 配置文件
```

## 🔍 調試技巧

1. **檢查中間數據**: 查看 `step1_data_*.json` 文件
2. **重新運行階段**: 刪除對應的中間文件，重新運行
3. **手動修改**: 可以手動編輯中間數據文件
4. **分步測試**: 每個階段都可以獨立測試 