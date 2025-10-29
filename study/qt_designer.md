python3 -m venv ~/venv/qt
source ~/venv/qt/bin/activate
pip install pyside6
export PYSIDE_DESIGNER_PLUGINS="/home/adg/github/hwidgets/plugins"

pip install -e ../hwidgets
pip install -e ../hutils

pyside6-designer

