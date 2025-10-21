pyside6-uic .\designer\ui_main_window.ui -o .\designer\ui_main_window.py
python ..\scripts\q_to_h.py .\designer\ui_main_window.py

python test_widgets.py
