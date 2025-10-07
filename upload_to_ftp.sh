#!/bin/bash

# FTP上傳腳本 - 將_site資料夾內容上傳到FTP伺服器
# 使用lftp進行批量上傳

# FTP設定
FTP_HOST="ftp.vericoglobal.com"
FTP_USER="webupdater@vericoglobal.com"
FTP_PASS="Pegasusy11221206"
LOCAL_DIR="_site"
REMOTE_DIR="/"

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

echo -e "${GREEN}所有檔案已成功上傳到FTP伺服器並覆蓋現有檔案。${NC}"
