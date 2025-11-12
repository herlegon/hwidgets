from PySide6.QtWidgets import QApplication, QWidget, QSplitter, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, QTimer

app = QApplication([])

# Panels
topPanel = QWidget()          # Top panel spanning col 1 + col 2
modelPanel = QWidget()        # First column
metaConvertPanel = QWidget()  # Second column
logViewer = QWidget()         # Third column (hideable, fixed width)

# Colors for demo
topPanel.setStyleSheet("background-color: lightyellow")
modelPanel.setStyleSheet("background-color: lightblue")
metaConvertPanel.setStyleSheet("background-color: lightgreen")
logViewer.setStyleSheet("background-color: lightgray")

# Horizontal splitter for bottom row (col 1 + col 2 + col 3)
bottomSplitter = QSplitter(Qt.Horizontal)
bottomSplitter.addWidget(modelPanel)
bottomSplitter.addWidget(metaConvertPanel)
bottomSplitter.addWidget(logViewer)

# Fixed widths
modelPanel.setFixedWidth(200)
logViewer.setFixedWidth(300)
logViewer.hide()  # initially hidden

# Make middle column stretch
bottomSplitter.setStretchFactor(1, 1)  # metaConvertPanel stretches

# Vertical layout: top panel + bottom splitter
mainLayout = QVBoxLayout()
mainLayout.addWidget(topPanel)
mainLayout.addWidget(bottomSplitter)

# Main window
window = QWidget()
window.setLayout(mainLayout)
window.resize(900, 500)
window.show()

# Function to toggle third column
def toggle_log():
    if logViewer.isHidden():
        logViewer.show()
    else:
        logViewer.hide()

# Example: toggle after 2 seconds
QTimer.singleShot(5000, toggle_log)

app.exec()
