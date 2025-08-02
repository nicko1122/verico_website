#!/bin/bash

# 切換到項目目錄
cd /home/nicko1122/webproject/verico

echo "🔄 重啟 Fastify Server..."
echo ""

# 先停止服務
echo "1️⃣ 停止現有服務..."
./stop_static_server.sh

echo ""
echo "2️⃣ 等待服務完全停止..."
sleep 3

echo ""
echo "3️⃣ 啟動服務..."
./start_static_server.sh 