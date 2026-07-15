### Product Manager 使用說明

本工具提供產品的「上傳生成、列表檢視、批次刪除（下架）」管理能力，與現有 `product-generator-v2` 完全相容。


### 啟動

> 2026-07 起建議改用 repo 根目錄的 `./admin.sh`(統一後台,含本工具全部功能 + Dashboard/Setup/Compose/Build/Deploy)。以下原啟動方式仍可用。

```bash
cd product-manager
./start_server.sh
```

預設埠：`http://localhost:5012/`


### 功能

- 上傳 ZIP 與備份
  - 僅接受 `.zip`，上傳後先存至 `product-manager/inbox/`
  - 立即複製一份到 `product-manager/backups/`，同名會覆蓋（永遠保留最新版）
  - 之後呼叫既有的 `process_zip_v2()` 完成解析/翻譯/生成

- 列表檢視
  - 掃描 `src/_data/products/*.yml`，依 `category` 分組顯示
  - 顯示：英文名稱、YAML 檔名、URL、圖片數量

- 批次刪除（下架）
  - 勾選產品並刪除，執行內容：
    - 刪除 `src/_data/products/{yaml}`
    - 刪除 `src/assets/images/product/{asset_slug}/` 整個資料夾
    - 從 `src/_data/products.yml` 移除 EN/DE 對應 URL 的卡片
  - 設計理念：ZIP 備份已保留，可隨時再上傳恢復


### 關鍵設計與相容行為

- 唯一鍵採用 YAML 檔名（對齊你目前的工作模式）
  - 上傳覆蓋條件：ZIP 檔名（去副檔名）同名 → 覆寫同一支 YAML
  - 頁面 URL 與資產資料夾仍以「英文名稱」的 slug 決定
- 刪除時的 `asset_slug` 由 YAML 內圖片路徑推導（`assets/images/product/{asset_slug}/...`）
- 產品分類鍵值（category）：`powerbank | loopenergy | gan_charger | flash_disk`


### API（內部使用）

- GET `/api/list`
  - 回傳 `{ ok, groups: { [category]: Product[] }, count }`
- POST `/api/delete`
  - 請求：`{ yaml_files: ["LoopEnergy-AA2550.yml", ...] }`
  - 回傳：`{ ok, deleted: string[], errors: {file,error}[] }`
- POST `/upload`
  - form-data: `file=@xxx.zip`
  - 回傳：`{ ok, product_url }`


### 注意事項

- 上線部署：此服務需 Python 環境（Flask）。僅用於後台工具，不需佈署到純靜態主機。
- 權限與安全：建議加上簡單密碼保護或限制內網存取；必要時可加入基本認證。
- 與生成器版本對齊：本服務直接呼叫 `product-generator-v2/processor_v2.py`，請確保該模組能在相同環境下執行。


