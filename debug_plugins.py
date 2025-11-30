
import os
import sys
import importlib
import traceback

# Add plugins directory to path
plugins_dir = os.path.join(os.getcwd(), 'qtdesigner', 'plugins')
sys.path.append(plugins_dir)

print(f"Checking plugins in: {plugins_dir}")

files = [f for f in os.listdir(plugins_dir) if f.endswith('_plugin.py')]

for f in files:
    module_name = f[:-3]
    print(f"Checking {module_name}...")
    try:
        module = importlib.import_module(module_name)
        print(f"  Imported {module_name}")

        # Find class that inherits from QDesignerCustomWidgetInterface
        # This part is tricky without QDesignerCustomWidgetInterface available if not in designer context?
        # But we have PySide6 installed, so we can import it.

        # We can just check if we can instantiate the class that matches the filename convention
        # e.g. button_group_plugin -> HButtonGroupPlugin?
        # Or just inspect the module.

    except Exception as e:
        print(f"  FAILED to import {module_name}: {e}")
        traceback.print_exc()
