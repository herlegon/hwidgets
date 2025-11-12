from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
)
from PySide6.QtCore import Qt

app = QApplication([])

# Panels
topPanel1 = QWidget()
topPanel2 = QWidget()
modelPanel = QWidget()
metaConvertPanel = QWidget()
logViewer = QWidget()

# Colors for clarity
topPanel1.setStyleSheet("background-color: lightyellow")
topPanel2.setStyleSheet("background-color: khaki")
modelPanel.setStyleSheet("background-color: lightblue")
metaConvertPanel.setStyleSheet("background-color: lightgreen")
logViewer.setStyleSheet("background-color: lightgray")

# -------------------
# Top Panel 1 layout (with log toggle button)
topLayout1 = QHBoxLayout(topPanel1)
toggleButton = QPushButton("Show/Hide Log")
topLayout1.addWidget(toggleButton)
topLayout1.addStretch()

# -------------------
# Top vertical section (two stacked panels)
topSection = QWidget()
topSectionLayout = QVBoxLayout(topSection)
topSectionLayout.setContentsMargins(0, 0, 0, 0)
topSectionLayout.addWidget(topPanel1)
topSectionLayout.addWidget(topPanel2)

# -------------------
# Bottom left (model + meta)
bottomLeft = QWidget()
bottomLeftLayout = QHBoxLayout(bottomLeft)
bottomLeftLayout.setContentsMargins(0, 0, 0, 0)
bottomLeftLayout.addWidget(modelPanel)
bottomLeftLayout.addWidget(metaConvertPanel)

modelPanel.setFixedWidth(200)  # fixed column 1
# metaConvertPanel expands automatically

# -------------------
# Combine top + bottom (left side)
leftSide = QWidget()
leftLayout = QVBoxLayout(leftSide)
leftLayout.setContentsMargins(0, 0, 0, 0)
leftLayout.addWidget(topSection)
leftLayout.addWidget(bottomLeft)

# -------------------
# Main horizontal layout (left side + log panel)
mainLayout = QHBoxLayout()
mainLayout.addWidget(leftSide)
mainLayout.addWidget(logViewer)
mainLayout.setSpacing(9)

logViewer.setFixedWidth(300)
logViewer.hide()

# -------------------
# Main window setup
window = QWidget()
window.setLayout(mainLayout)
window.resize(900, 600)
window.show()

# -------------------
# Toggle log panel by resizing the window
def toggle_log():
    log_width = logViewer.width()
    window_width = window.width()
    if logViewer.isHidden():
        logViewer.show()
        window.resize(window_width + log_width + 9, window.height())
    else:
        window.resize(window_width - log_width - 9, window.height())
        logViewer.hide()

toggleButton.clicked.connect(toggle_log)

app.exec()
