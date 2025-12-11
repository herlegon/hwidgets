import signal

from pathlib import Path
from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl
import platform
import subprocess

def open_file_location(filepath: Path):
    """Open file explorer and select the specified file."""
    if not filepath.exists():
        print(f"File does not exist: {filepath}")
        return

    system = platform.system()

    try:
        if system == "Windows":
            # Use explorer with /select flag
            subprocess.run(['explorer', '/select,', str(filepath.absolute())])
        elif system == "Darwin":  # macOS
            subprocess.run(['open', '-R', str(filepath.absolute())])
        elif system == "Linux":
            # Linux file managers vary, try common ones
            # Most Linux file managers don't support selecting a file,
            # so we open the parent directory instead
            parent_dir = filepath.parent
            try:
                # Try with dbus (works with some file managers like Nautilus)
                subprocess.run(['dbus-send', '--session', '--dest=org.freedesktop.FileManager1',
                              '--type=method_call', '/org/freedesktop/FileManager1',
                              'org.freedesktop.FileManager1.ShowItems',
                              f'array:string:file://{filepath.absolute()}', 'string:'])
            except FileNotFoundError:
                # Fallback: just open the directory
                QDesktopServices.openUrl(QUrl.fromLocalFile(str(parent_dir)))
    except Exception as e:
        print(f"Error opening file location: {e}")

# Usage example:
# button.clicked.connect(lambda: open_file_location(your_path))




from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
from pathlib import Path





if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)


    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout()

    my_file = Path("/home/adg/github/hwss/server.log")

    button = QPushButton("Show File in Explorer")
    button.clicked.connect(lambda: open_file_location(my_file))

    layout.addWidget(button)
    window.setLayout(layout)
    window.show()
    app.exec()
