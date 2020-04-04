#!/bin/bash
source /home/ubuntu/etfenv/bin/activate
cd /home/ubuntu/ETFAnalysis/ || exit
python ProcessCaller.py
wait $(pidof python)
python /home/ubuntu/ETFAnalysis/CalculateETFArbitrage/Caller.py