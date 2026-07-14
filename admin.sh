#!/usr/bin/env bash
# Verico Admin 單一入口:自建 venv、裝依賴、啟動後台(預設 http://localhost:5012/)
# 遠端機器(如 core)使用時:ssh -L 5012:localhost:5012 <host> 再開本機瀏覽器
set -euo pipefail
cd "$(dirname "$0")/product-manager"
python3 -m venv .venv 2>/dev/null || true
source .venv/bin/activate
pip install -q flask pyyaml python-dotenv openai
echo ""
echo "  Verico Admin  ->  http://localhost:${ADMIN_PORT:-5012}/"
echo ""
exec python server.py
