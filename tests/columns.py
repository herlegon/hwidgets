from PySide6.QtWidgets import QApplication, QWidget, QSplitter, QVBoxLayout
from PySide6.QtCore import Qt, QTimer

app = QApplication([])

# Panels
modelPanel = QWidget()        # First column (fixed)
metaConvertPanel = QWidget()  # Second column (resizable)
logViewer = QWidget()         # Third column (fixed width, hideable)

# Example colors for visibility
modelPanel.setStyleSheet("background-color: lightblue")
metaConvertPanel.setStyleSheet("background-color: lightgreen")
logViewer.setStyleSheet("background-color: lightgray")

# Splitter
splitter = QSplitter(Qt.Horizontal)
splitter.addWidget(modelPanel)
splitter.addWidget(metaConvertPanel)
splitter.addWidget(logViewer)

# Fix widths
modelPanel.setFixedWidth(200)   # first column fixed
logViewer.setFixedWidth(300)    # third column fixed

# Initially hide third column
logViewer.hide()

# Layout
window = QWidget()
layout = QVBoxLayout(window)
layout.addWidget(splitter)
window.resize(900, 500)
window.show()

# Function to toggle third column
def toggle_log():
    if logViewer.isHidden():
        logViewer.show()
    else:
        logViewer.hide()

# Example: toggle after 2 seconds
QTimer.singleShot(2000, toggle_log)

app.exec()
