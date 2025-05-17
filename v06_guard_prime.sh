#!/bin/bash
# v06_guard_prime.sh - 背景守護腳本，確保 ultracore 實時掛機不中斷

LOG_PATH="/mnt/data/ai/logs/guard_log.txt"
TARGET_SCRIPT="/mnt/data/ai/v05_ultracore_real_prime.py"

while true
do
    RUNNING=$(ps aux | grep "$TARGET_SCRIPT" | grep -v grep)
    if [ -z "$RUNNING" ]; then
        echo "[guard] 偵測到主控未執行，重新啟動中..." >> $LOG_PATH
        nohup python3 $TARGET_SCRIPT >> $LOG_PATH 2>&1 &
    else
        echo "[guard] 主控正常執行中。" >> $LOG_PATH
    fi
    sleep 60
done
