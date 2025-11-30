pyside6-uic .\designer\ui_main_window.ui -o .\designer\ui_main_window.py
python ..\..\scripts\patch_icons_dir.py .\designer\ui_main_window.py

python test_qwidgets.py
