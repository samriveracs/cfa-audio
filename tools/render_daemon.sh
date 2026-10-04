#!/bin/bash
# Render episodes in order once their review note exists. Stops when no work remains for 3 hours.
cd /home/claude/podcast
idle=0
while true; do
  did=0
  for n in $(seq 1 48); do
    e=$(printf "E%02d" $n)
    if [ -f scripts/$e.txt ] && [ -f reviews/$e.md ] && [ ! -f audio/$e.mp3 ] && [ ! -f audio/$e.hold ]; then
      python3 bin/tts_episode.py $n || echo "{\"ep\": $n, \"error\": true}"
      did=1; break
    fi
  done
  if [ $did -eq 0 ]; then idle=$((idle+1)); sleep 60; else idle=0; fi
  [ $idle -gt 180 ] && break
done
