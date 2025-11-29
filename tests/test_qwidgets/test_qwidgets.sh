#!/usr/bin/env bash
set -e  # exit immediately on error

SKIP_UI=false

# Parse arguments
for arg in "$@"; do
    case $arg in
        --skip-ui)
            SKIP_UI=true
            shift
            ;;
        *)
            shift
            ;;
    esac
done

# === UI generation section ===
if [ "$SKIP_UI" = false ]; then
    pyside6-uic ./designer/ui_main_window.ui -o ./designer/ui_main_window.py
    python ../../scripts/patch_icons_dir.py ./designer/ui_main_window.py
    # python ../../scripts/q_to_h.py ./designer/ui_main_window.py
else
    echo "Skipping UI generation (--skip-ui flag detected)"

fi

export QT_QPA_PLATFORM=xcb
python test_qwidgets.py

