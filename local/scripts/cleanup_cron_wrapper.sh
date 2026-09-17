#!/bin/bash
# Run cleanup only every 3 days; stamp file tracks last run.
STAMP="/Users/adwit.sharma/kb_docs/local/.cleanup_last_run"
NOW=$(date +%s)

if [ -f "$STAMP" ]; then
    LAST=$(cat "$STAMP")
    DIFF=$(( (NOW - LAST) / 86400 ))
    if [ "$DIFF" -lt 3 ]; then
        exit 0
    fi
fi

echo "$NOW" > "$STAMP"
bash /Users/adwit.sharma/kb_docs/local/scripts/cleanup_old_data.sh >> /Users/adwit.sharma/kb_docs/local/supervisor/logs/cleanup.log 2>&1
