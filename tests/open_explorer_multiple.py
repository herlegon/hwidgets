import shutil
import signal

from pathlib import Path
from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl
import platform
import subprocess

from pathlib import Path
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl
import platform
import subprocess

from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
from pathlib import Path




def open_file_location_multiple(filepaths: list[Path]):
    """Open file explorer and select multiple files."""
    # Filter out non-existent files
    existing_files = [fp for fp in filepaths if fp.exists()]
    print(existing_files)

    if not existing_files:
        print("No valid files to show")
        return

    system = platform.system()

    try:
        if system == "Windows":
            # Windows explorer can select multiple files with /select
            # All files must be in the same directory
            parent_dir = existing_files[0].parent

            # Check if all files are in the same directory
            if all(fp.parent == parent_dir for fp in existing_files):
                # Use comma-separated paths
                file_args = ','.join(str(fp.absolute()) for fp in existing_files)
                subprocess.run(['explorer', '/select,', file_args])
            else:
                print("Files are in different directories, opening first file only")
                subprocess.run(['explorer', '/select,', str(existing_files[0].absolute())])

        elif system == "Darwin":  # macOS
            # macOS Finder supports multiple file selection
            args = ['open', '-R'] + [str(fp.absolute()) for fp in existing_files]
            subprocess.run(args)

        elif system == "Linux":

            if shutil.which('gdbus'):
                print("gdbus")
                try:
                    file_uris = [fp.as_uri() for fp in existing_files]
                    # Use gdbus instead of dbus-send - it's more reliable
                    subprocess.run([
                        'gdbus', 'call', '--session',
                        '--dest', 'org.freedesktop.FileManager1',
                        '--object-path', '/org/freedesktop/FileManager1',
                        '--method', 'org.freedesktop.FileManager1.ShowItems',
                        str(file_uris), ''
                    ], check=True)
                    return  # Success!
                except subprocess.CalledProcessError as e:
                    print(f"D-Bus method failed: {e}")
                return

            # Detect which file manager is running
            file_manager = None

            # Check common file managers
            if shutil.which('nemo'):
                file_manager = 'nemo'
            elif shutil.which('nautilus'):
                file_manager = 'nautilus'
            elif shutil.which('dolphin'):
                file_manager = 'dolphin'
            elif shutil.which('thunar'):
                file_manager = 'thunar'

            print(file_manager)

            file_uris = [fp.as_uri() for fp in existing_files]
            subprocess.Popen(['nautilus', '--select'] + file_uris)


            # if file_manager == 'nemo':
            #     # Nemo doesn't natively support selecting multiple files
            #     # Use a script approach with xdotool or just open with files highlighted
            #     file_uris = [fp.as_uri() for fp in existing_files]

            #     # Open nemo with the files - they will be selected
            #     command = ['nemo'] + [str(fp.absolute()) for fp in existing_files]
            #     print(command)
            #     subprocess.Popen(command)



            # elif file_manager == 'nautilus':
            #     file_uris = [f'file://{fp.absolute()}' for fp in existing_files]
            #     subprocess.Popen(['nautilus', '--select'] + file_uris)
            # elif file_manager == 'dolphin':
            #     file_paths = [str(fp.absolute()) for fp in existing_files]
            #     subprocess.Popen(['dolphin', '--select'] + file_paths)
            # elif file_manager == 'thunar':
            #     # Thunar doesn't support multi-select well, open parent dir
            #     parent = existing_files[0].parent
            #     subprocess.Popen(['thunar', str(parent)])
            # else:

            #     # else:
            #     print("D-BUS")
            #     # Linux with D-Bus supports multiple files
            #     if shutil.which('dbus-send'):
            #         try:
            #             # Build the file URI array properly for D-Bus
            #             file_uris = [f'file://{fp.absolute()}' for fp in existing_files]

            #             # Construct the array as separate arguments
            #             dbus_cmd = [
            #                 'dbus-send',
            #                 '--session',
            #                 '--print-reply',
            #                 '--dest=org.freedesktop.FileManager1',
            #                 '/org/freedesktop/FileManager1',
            #                 'org.freedesktop.FileManager1.ShowItems',
            #                 f'array:string:{",".join(file_uris)}',
            #                 'string:'
            #             ]
            #             print(dbus_cmd)

            #             subprocess.run(dbus_cmd)
            #         except Exception as e:
            #             print(f"D-Bus error: {e}")
            #             # Fallback: open parent directory
            #             QDesktopServices.openUrl(QUrl.fromLocalFile(str(existing_files[0].parent)))
            #     else:
            #         # Final fallback: open parent directory
            #         QDesktopServices.openUrl(QUrl.fromLocalFile(str(existing_files[0].parent)))




    except Exception as e:
        print(f"Error opening file locations: {e}")


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)


    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout()

    my_files = [
        Path("/home/adg/github/hwss/server.log"),
        Path("/home/adg/github/hwss/LOGGING.md"),
    ]

    button = QPushButton("Show Multiple Files in Explorer")
    button.clicked.connect(lambda: open_file_location_multiple(my_files))

    layout.addWidget(button)
    window.setLayout(layout)
    window.show()
    app.exec()
