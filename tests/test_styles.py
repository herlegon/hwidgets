
# ===== USAGE =====
# style = StyleManager.get_style("dark")
# style = StyleManager.get_style("blue")
# available = StyleManager.list_schemes()  # ["dark", "blue", "zen"]
from pathlib import Path
from pprint import pprint
import signal
import sys
package_path = str(Path(__file__).resolve().parent.parent / 'hwidgets')
print(package_path)
sys.path.append(package_path)

from hwidgets import (
    StyleManager,
)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    style = StyleManager.get_theme()
    available = StyleManager.list_schemes()

    pprint(style)
