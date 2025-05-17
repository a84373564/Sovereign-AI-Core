#!/bin/bash
# v07_start_prime.sh - 一鍵啟動整個 Sovereign 系統主控與守護

echo "[start] 啟動守護程序..."
nohup bash /mnt/data/ai/v06_guard_prime.sh >> /mnt/data/ai/logs/guard_log.txt 2>&1 &

sleep 2

echo "[start] 所有系統掛機程序已啟動完成！"
