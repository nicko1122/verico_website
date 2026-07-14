#!/bin/bash

# checksum-manifest 上傳腳本
# 流程：計算本地 _site 的 sha1 清單 -> 下載遠端 .site_manifest.json -> 比對 -> 只上傳差異檔案 -> 更新遠端 manifest

FTP_HOST="ftp.vericoglobal.com"
FTP_USER="webupdater@vericoglobal.com"
FTP_PASS="Pegasusy11221206"
LOCAL_DIR="_site"
MANIFEST_REMOTE=".site_manifest.json"
MANIFEST_LOCAL="/tmp/site_manifest_local.json"
MANIFEST_REMOTE_LOCAL="/tmp/site_manifest_remote.json"
DRY_RUN=0
PARALLEL=8

usage(){
  echo "Usage: $0 [--dry-run] [--parallel N]"
  exit 1
}

while [ "$1" != "" ]; do
  case "$1" in
    --dry-run) DRY_RUN=1 ;; 
    --parallel) shift; PARALLEL=$1 ;; 
    -h|--help) usage ;; 
    *) usage ;;
  esac
  shift
done

if [ ! -d "$LOCAL_DIR" ]; then
  echo "ERROR: $LOCAL_DIR not found"
  exit 1
fi

# 1) 產生本地 manifest
python3 - <<PY > "$MANIFEST_LOCAL"
import os,sys,hashlib,json
root='''$LOCAL_DIR'''
out={}
for dirpath,dirnames,filenames in os.walk(root):
    for f in filenames:
        p=os.path.join(dirpath,f)
        rel=os.path.relpath(p,root).replace('\\\\','/')
        h=hashlib.sha1()
        try:
            with open(p,'rb') as fh:
                while True:
                    chunk=fh.read(8192)
                    if not chunk: break
                    h.update(chunk)
            out[rel]=h.hexdigest()
        except Exception as e:
            print('WARN',p,e,file=sys.stderr)
json.dump(out,sys.stdout,ensure_ascii=False,indent=2)
PY

# 2) 下載遠端 manifest（如果存在）
rm -f "$MANIFEST_REMOTE_LOCAL"
lftp -u "$FTP_USER,$FTP_PASS" "$FTP_HOST" -e "set ssl:verify-certificate no; get $MANIFEST_REMOTE -o $MANIFEST_REMOTE_LOCAL; quit" 2>/dev/null || true

# 3) 計算差異檔案（使用 Python） -> 輸出 null 分隔的路徑清單
UPLOAD_LIST="/tmp/site_to_upload.txt"
python3 - <<PY > "$UPLOAD_LIST"
import json,sys
local=json.load(open('$MANIFEST_LOCAL','r'))
remote={}
try:
    remote=json.load(open('$MANIFEST_REMOTE_LOCAL','r'))
except Exception:
    remote={}

# files to upload: in local and (not in remote or checksum differs)
out=[]
for k,v in local.items():
    if k not in remote or remote.get(k)!=v:
        out.append(k)
# print null-separated
if out:
    sys.stdout.write('\0'.join(out))

PY

# Count files
if [ -s "$UPLOAD_LIST" ]; then
  FILE_COUNT=$(tr -dc '\\0' < "$UPLOAD_LIST" | wc -c)
  # above counts nulls; more reliable to use python again
  FILE_COUNT=$(python3 - <<PY
s=open('$UPLOAD_LIST','rb').read()
if not s: print(0)
else: print(len(s.split(b'\\0')))
PY
)
else
  FILE_COUNT=0
fi

echo "Local files: $(jq -r 'keys | length' $MANIFEST_LOCAL 2>/dev/null || echo '?')"
echo "Remote manifest found: $( [ -s $MANIFEST_REMOTE_LOCAL ] && echo yes || echo no )"
echo "Files to upload: $FILE_COUNT"

if [ "$FILE_COUNT" -eq 0 ]; then
  echo "Nothing to upload."
  exit 0
fi

if [ "$DRY_RUN" -eq 1 ]; then
  echo "Dry run - listing files to upload:" 
  python3 - <<PY
s=open('$UPLOAD_LIST','rb').read()
if s:
    for p in s.split(b'\\0'):
        if p: print(p.decode('utf-8'))
PY
  exit 0
fi

# 4) 上傳檔案 (使用 curl --ftp-create-dirs 並行)
export FTP_USER FTP_PASS FTP_HOST LOCAL_DIR
python3 - <<PY > /tmp/site_to_upload_commands.sh
import os,sys
s=open('$UPLOAD_LIST','rb').read()
if not s:
    sys.exit(0)
for p in s.split(b'\\0'):
    if not p: continue
    path=p.decode('utf-8')
    local_path=os.path.join('$LOCAL_DIR',path)
    # escape single quotes by replacing '\\' with '\\\\' etc not necessary for curl
    print("curl -sS --ftp-create-dirs -u '"+"$FTP_USER"+":"+"$FTP_PASS"+"' -T \""+local_path+"\" \"ftp://"+"$FTP_HOST"+"/"+path+"\"")
PY

# run commands in parallel
chmod +x /tmp/site_to_upload_commands.sh || true
cat /tmp/site_to_upload_commands.sh | xargs -0 -I CMD -n1 -P $PARALLEL bash -c "CMD"

# 5) 上傳新的 manifest
curl -sS --ftp-create-dirs -u "$FTP_USER:$FTP_PASS" -T "$MANIFEST_LOCAL" "ftp://$FTP_HOST/$MANIFEST_REMOTE"

if [ $? -eq 0 ]; then
  echo "Upload completed and manifest updated."
  exit 0
else
  echo "Upload finished but manifest update failed."
  exit 1
fi
