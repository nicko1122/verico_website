#!/bin/bash

# 切換到項目目錄
cd /home/nicko1122/webproject/verico

echo "正在停止 Fastify Server..."

# 查找並停止 node server.js 進程
PIDS=$(ps aux | grep "node server.js" | grep -v grep | awk '{print $2}')

if [ -z "$PIDS" ]; then
    echo "❌ 沒有找到正在運行的 Fastify Server"
    echo "服務可能已經停止或不存在"
else
    echo "找到以下進程:"
    ps aux | grep "node server.js" | grep -v grep
    
    echo ""
    echo "正在停止進程..."
    for PID in $PIDS; do
        echo "停止進程 $PID..."
        kill $PID
    done
    
    # 等待進程完全停止
    sleep 2
    
    # 檢查是否還有進程在運行
    REMAINING=$(ps aux | grep "node server.js" | grep -v grep | awk '{print $2}')
    if [ -z "$REMAINING" ]; then
        echo "✅ Fastify Server 已成功停止"
    else
        echo "⚠️  部分進程仍在運行，強制停止..."
        for PID in $REMAINING; do
            kill -9 $PID
        done
        echo "✅ Fastify Server 已強制停止"
    fi
fi

echo ""
echo "服務狀態檢查:"
if curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo "❌ 服務仍在運行 (端口 8080)"
else
    echo "✅ 服務已停止 (端口 8080)"
fi 