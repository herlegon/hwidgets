pyside6-uic ./designer/ui_main_window.ui -o ./designer/ui_main_window.py
python ../../scripts/patch_icons_dir.py ./designer/ui_main_window.py
python ../../scripts/q_to_h.py ./designer/ui_main_window.py

export QT_QPA_PLATFORM=xcb
python test_widgets.py

