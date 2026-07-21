#!/bin/bash

# FTP上傳腳本 - 將_site資料夾內容上傳到FTP伺服器
# 使用lftp進行批量上傳
# 設定來源:repo 根目錄 .env(參考 .env.example)

# --- 載入設定 ---
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -f "$SCRIPT_DIR/.env" ]; then
  set -a
  . "$SCRIPT_DIR/.env"
  set +a
fi
: "${FTP_HOST:?未設定 FTP_HOST — 請執行 cp .env.example .env 並填入 FTP 設定}"
: "${FTP_USER:?未設定 FTP_USER — 請執行 cp .env.example .env 並填入 FTP 設定}"
: "${FTP_PASS:?未設定 FTP_PASS — 請執行 cp .env.example .env 並填入 FTP 設定}"
LOCAL_DIR="_site"
REMOTE_DIR="${FTP_REMOTE_DIR:-/}"

# 顏色輸出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}開始上傳_site資料夾到FTP伺服器...${NC}"

# 檢查本地_site目錄是否存在
if [ ! -d "$LOCAL_DIR" ]; then
    echo -e "${RED}錯誤: 找不到_site目錄！${NC}"
    exit 1
fi

# 使用lftp進行上傳
lftp -u "$FTP_USER,$FTP_PASS" "$FTP_HOST" << EOF
# 設定SSL證書驗證為否（避免證書問題）
set ssl:verify-certificate no

# 切換到遠端目錄
cd $REMOTE_DIR

# 使用mirror命令上傳整個目錄，覆蓋現有檔案
# -R: 反向mirror（上傳到遠端）
# -c: 繼續中斷的傳輸
# -e: 刪除遠端多餘的檔案
# -v: 詳細輸出
# --delete: 刪除遠端多餘檔案
# --overwrite: 覆蓋現有檔案
# --exclude-glob: 排除特定檔案
mirror -R -c -e -v --delete --overwrite --exclude-glob=".*" $LOCAL_DIR .

# 顯示上傳完成訊息
echo "上傳完成！"

# 退出lftp
quit
EOF

# 檢查上傳結果
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 上傳成功完成！${NC}"
else
    echo -e "${RED}❌ 上傳過程中發生錯誤！${NC}"
    exit 1
fi

# --- 上傳源資料快照(災難還原用:線上網站自帶 src/_data,restore_from_site.sh 可取回)---
SNAP="/tmp/verico_source_snapshot.tar.gz"
INFO="/tmp/SNAPSHOT_INFO.txt"
{
    echo "commit: $(git -C "$SCRIPT_DIR" rev-parse HEAD 2>/dev/null || echo unknown)"
    echo "branch: $(git -C "$SCRIPT_DIR" rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
    echo "date_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "uncommitted_changes: $(git -C "$SCRIPT_DIR" status --porcelain 2>/dev/null | wc -l)"
} > "$INFO"
if tar -czf "$SNAP" -C "$SCRIPT_DIR" src/_data -C /tmp SNAPSHOT_INFO.txt; then
    if curl -sS --ftp-create-dirs -u "$FTP_USER:$FTP_PASS" -T "$SNAP" "ftp://$FTP_HOST/.source_snapshot.tar.gz"; then
        echo -e "${GREEN}源資料快照已上傳(.source_snapshot.tar.gz)${NC}"
    else
        echo -e "${YELLOW}警告: 快照上傳失敗(網站已部署成功,但線上還原快照未更新)${NC}"
    fi
fi

echo -e "${GREEN}所有檔案已成功上傳到FTP伺服器並覆蓋現有檔案。${NC}"
