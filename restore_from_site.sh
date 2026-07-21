#!/bin/bash

# 災難還原:從線上網站取回源資料
# 來源 1:FTP 根目錄的 .source_snapshot.tar.gz(部署腳本自動維護,內含 src/_data + SNAPSHOT_INFO)
# 來源 2:--from-file 指定本地快照檔
# 用法: ./restore_from_site.sh [--dry-run] [--yes] [--with-images] [--from-file FILE]
#   --dry-run      只下載並顯示快照資訊與差異,不改任何東西
#   --yes          跳過互動確認(後台呼叫用)
#   --with-images  另外從線上 assets/images/product 鏡像回 src/assets/images/product(需 lftp)
#   --from-file F  不下載,直接用本地快照檔 F

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
if [ -f .env ]; then
  set -a
  . ./.env
  set +a
fi

DRY=0; YES=0; WITH_IMAGES=0; FROM_FILE=""
while [ "$1" != "" ]; do
  case "$1" in
    --dry-run) DRY=1 ;;
    --yes) YES=1 ;;
    --with-images) WITH_IMAGES=1 ;;
    --from-file) shift; FROM_FILE=$1 ;;
    -h|--help|*) echo "Usage: $0 [--dry-run] [--yes] [--with-images] [--from-file FILE]"; exit 1 ;;
  esac
  shift
done

SNAP="/tmp/verico_restore_snapshot.tar.gz"
WORK="/tmp/verico_restore_work"

if [ -n "$FROM_FILE" ]; then
  [ -f "$FROM_FILE" ] || { echo "ERROR: 找不到檔案 $FROM_FILE"; exit 1; }
  cp "$FROM_FILE" "$SNAP"
  echo "使用本地快照:$FROM_FILE"
else
  : "${FTP_HOST:?未設定 FTP_HOST — 請先設定 .env(cp .env.example .env 或後台 Setup)}"
  : "${FTP_USER:?未設定 FTP_USER — 請先設定 .env}"
  : "${FTP_PASS:?未設定 FTP_PASS — 請先設定 .env}"
  echo "從 ftp://$FTP_HOST 下載快照…"
  if ! curl -sS -f -u "$FTP_USER:$FTP_PASS" "ftp://$FTP_HOST/.source_snapshot.tar.gz" -o "$SNAP"; then
    echo "ERROR: 下載失敗 — 線上可能尚無快照(需先用含快照功能的部署腳本部署一次),或 FTP 設定錯誤"
    exit 1
  fi
fi

rm -rf "$WORK"
mkdir -p "$WORK"
tar -xzf "$SNAP" -C "$WORK" || { echo "ERROR: 快照解壓失敗(檔案損壞?)"; exit 1; }
[ -d "$WORK/src/_data" ] || { echo "ERROR: 快照內沒有 src/_data,格式不符"; exit 1; }

echo ""
echo "=== 快照資訊 ==="
cat "$WORK/SNAPSHOT_INFO.txt" 2>/dev/null || echo "(無 SNAPSHOT_INFO)"
echo ""
echo "=== 快照 vs 本地 src/_data 差異 ==="
DIFF_OUT=$(diff -rq "$WORK/src/_data" src/_data 2>&1)
if [ -z "$DIFF_OUT" ]; then
  echo "(完全一致 — 本地資料已是線上版本,無需還原)"
else
  echo "$DIFF_OUT" | sed -e "s|$WORK/src/_data|快照|" -e "s|src/_data|本地|" | head -40
  echo "(差異項目數: $(echo "$DIFF_OUT" | wc -l))"
fi
echo ""

if [ "$DRY" -eq 1 ]; then
  echo "[dry-run] 未做任何變更。要執行還原請去掉 --dry-run"
  exit 0
fi

if [ "$YES" -ne 1 ]; then
  printf "確定用快照覆蓋本地 src/_data ?(本地獨有的檔案會保留)[y/N] "
  read -r ans
  [ "$ans" = "y" ] || [ "$ans" = "Y" ] || { echo "已取消"; exit 0; }
fi

cp -a "$WORK/src/_data/." src/_data/
echo "✅ src/_data 已從快照還原"

if [ "$WITH_IMAGES" -eq 1 ]; then
  : "${FTP_HOST:?--with-images 需要 FTP 設定}"
  command -v lftp >/dev/null 2>&1 || { echo "ERROR: --with-images 需要 lftp(sudo apt install lftp)"; exit 1; }
  echo "從線上鏡像回產品圖(assets/images/product → src/assets/images/product)…"
  mkdir -p src/assets/images/product
  lftp -u "$FTP_USER,$FTP_PASS" "$FTP_HOST" -e "set ssl:verify-certificate no; mirror --verbose assets/images/product src/assets/images/product; quit"
  echo "✅ 產品圖已取回"
fi

echo ""
echo "完成 — 請檢查內容,確認後 git add / commit / push,把資料收回版本控制"
