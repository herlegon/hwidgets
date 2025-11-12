from PySide6.QtWidgets import (
    QApplication, QWidget, QSplitter, QVBoxLayout, QHBoxLayout, QPushButton
)
from PySide6.QtCore import Qt

app = QApplication([])

# Panels
topPanel1 = QWidget()
topPanel2 = QWidget()
modelPanel = QWidget()
metaConvertPanel = QWidget()
logViewer = QWidget()

# Colors for visibility
topPanel1.setStyleSheet("background-color: lightyellow")
topPanel2.setStyleSheet("background-color: khaki")
modelPanel.setStyleSheet("background-color: lightblue")
metaConvertPanel.setStyleSheet("background-color: lightgreen")
logViewer.setStyleSheet("background-color: lightgray")

# -------------------
# Top panel 1 layout with toggle button
topLayout = QHBoxLayout(topPanel1)
toggleButton = QPushButton("Show/Hide Log")
topLayout.addWidget(toggleButton)
topLayout.addStretch()
topPanel1.setFixedHeight(50)

# -------------------
# Create top vertical splitter for the 2 stacked top panels
topSplitter = QSplitter(Qt.Vertical)
topSplitter.addWidget(topPanel1)
topSplitter.addWidget(topPanel2)
topSplitter.setStretchFactor(1, 1)
topPanel2.setMinimumHeight(50)

# -------------------
# Bottom left area: model + meta columns
leftBottomSplitter = QSplitter(Qt.Horizontal)
leftBottomSplitter.addWidget(modelPanel)
leftBottomSplitter.addWidget(metaConvertPanel)
leftBottomSplitter.setStretchFactor(1, 1)
modelPanel.setFixedWidth(200)

# -------------------
# Left side (vertical): 2 top panels + bottom columns
leftSplitter = QSplitter(Qt.Vertical)
leftSplitter.addWidget(topSplitter)
leftSplitter.addWidget(leftBottomSplitter)
leftSplitter.setStretchFactor(1, 1)

# -------------------
# Main horizontal splitter: left side + log panel
mainSplitter = QSplitter(Qt.Horizontal)
mainSplitter.addWidget(leftSplitter)
mainSplitter.addWidget(logViewer)
logViewer.setFixedWidth(300)
logViewer.hide()

# -------------------
# Main window layout
window = QWidget()
layout = QVBoxLayout(window)
layout.addWidget(mainSplitter)
window.resize(900, 600)
window.show()

# -------------------
# Button callback to toggle log panel by resizing window
def toggle_log():
    log_width = logViewer.width()
    window_width = window.width()
    if logViewer.isHidden():
        logViewer.show()
        window.resize(window_width + log_width, window.height())
    else:
        window.resize(window_width - log_width, window.height())
        logViewer.hide()

toggleButton.clicked.connect(toggle_log)

app.exec()
