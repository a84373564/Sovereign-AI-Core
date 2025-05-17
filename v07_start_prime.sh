#!/bin/bash
# v07_start_prime.sh — 一鍵啟動整個系統核心（ultracore + guard + monitor）

echo "[start] 啟動主控 ultracore_real_prime.py..."
nohup python3 /mnt/data/ai/v05_ultracore_real_prime.py > /mnt/data/ai/logs/ultracore.log 2>&1 &

sleep 2

echo "[start] 啟動守護 v06_guard_prime.sh..."
nohup bash /mnt/data/ai/v06_guard_prime.sh > /mnt/data/ai/logs/guard.log 2>&1 &

sleep 2

echo "[start] 啟動監控介面 monitor_prime.py..."
nohup python3 /mnt/data/ai/monitor_prime.py > /mnt/data/ai/logs/monitor.log 2>&1 &

echo "[start] 所有系統掛機程序已啟動完成"
