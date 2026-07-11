#!/bin/bash
osascript <<EOF
tell application "Terminal"
    activate
    do script "cd '$PWD' && source .venv/bin/activate && python ./src/panel_editor.py $@"
end tell
EOF
