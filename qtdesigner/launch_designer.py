# launch_designer.py
import os
import subprocess
import sys

# Set plugin path
plugin_path = r"A:\hwidgets\qtdesigner"
# plugins_path = os.path.join(os.path.dirname(__file__))
sys.path.append(plugin_path)
sys.path.append(r"A:\hwidgets")
os.environ["PYSIDE_DESIGNER_PLUGINS"] = plugin_path

# Launch designer using subprocess
try:
    subprocess.run(["pyside6-designer"], check=True)
except FileNotFoundError:
    print("Error: pyside6-designer not found. Make sure PySide6 is installed.")
    sys.exit(1)
