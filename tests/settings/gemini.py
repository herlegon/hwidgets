import sys
import random
from PySide6.QtCore import Qt, QSize, QPoint
from PySide6.QtGui import QColor, QPainter, QPen, QBrush
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QWidget, QFormLayout,
    QComboBox, QLineEdit, QFrame, QSizePolicy, QCheckBox
)

# --- Custom Components ---

class ToggleSwitch(QCheckBox):
    """
    A custom QCheckBox styled to look like a horizontal toggle switch (HSwitch).
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(40, 24)
        self.setCursor(Qt.PointingHandCursor)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        # Colors
        track_color = QColor("#bdc3c7")
        thumb_color = QColor("#ecf0f1")
        if self.isChecked():
            track_color = QColor("#2ecc71") # Green when active

        # Draw Track
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(track_color))
        p.drawRoundedRect(0, 0, self.width(), self.height(), 12, 12)

        # Draw Thumb
        p.setBrush(QBrush(thumb_color))
        radius = 10
        y = (self.height() - radius * 2) / 2
        if self.isChecked():
            x = self.width() - (radius * 2) - 2
        else:
            x = 2
        p.drawEllipse(x, y, radius * 2, radius * 2)
        p.end()

class FramelessSettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        # 1. Window Flags: Frameless, Dialog
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setModal(True) # This prevents interaction with the main window

        # Style the dialog (give it a border since it has no frame)
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                border: 1px solid #999;
            }
            QLabel { font-size: 12px; }
            QComboBox, QLineEdit { padding: 4px; }
            QPushButton { padding: 6px 12px; }
        """)

        # --- Main Layout ---
        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2) # Thin margin for the border

        # Inner container for content (to have white background inside border)
        content_container = QWidget()
        content_container.setStyleSheet("background-color: white;")
        layout.addWidget(content_container)

        v_layout = QVBoxLayout(content_container)

        # --- Header ---
        header_lbl = QLabel("Application Settings")
        header_lbl.setStyleSheet("font-weight: bold; font-size: 14px; padding: 10px;")
        header_lbl.setAlignment(Qt.AlignCenter)
        v_layout.addWidget(header_lbl)

        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        v_layout.addWidget(line)

        # --- Scroll Area ---
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)

        # The widget inside the scroll area
        self.settings_widget = QWidget()
        self.form_layout = QFormLayout(self.settings_widget)
        self.form_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.form_layout.setContentsMargins(20, 20, 30, 20)
        self.form_layout.setVerticalSpacing(15)

        # --- Adding Specific Settings ---

        # 1. Reload previous model
        self.form_layout.addRow("Reload previous model:", ToggleSwitch())

        # 2. Default Graphic Card (Read Only)
        self.cb_gpu = QComboBox()
        self.cb_gpu.addItems(["NVIDIA RTX 3080", "NVIDIA RTX 4090", "Integrated Graphics"])
        self.cb_gpu.setEnabled(False) # Read only visually
        # Alternatively setEditable(False) is default, but setEnabled(False) grays it out.
        # If you want it selectable but not type-able, standard QComboBox is already that.
        self.form_layout.addRow("Default GPU:", self.cb_gpu)

        # 3. Persistent Output Folder (Editable + Browse)
        folder_layout = QHBoxLayout()
        self.folder_edit = QComboBox() # Requested as Editable Combobox
        self.folder_edit.setEditable(True)
        self.folder_edit.addItems(["C:/Outputs/v1", "D:/Project/Render"])
        btn_browse = QPushButton("Browse...")
        folder_layout.addWidget(self.folder_edit)
        folder_layout.addWidget(btn_browse)
        self.form_layout.addRow("Output Folder:", folder_layout)

        # 4. Default Values Group (Sub-headers or items)
        self.form_layout.addRow(QLabel("<b>Default Values:</b>"))

        self.cb_onnx = QComboBox()
        self.cb_onnx.addItems(["Opset 16", "Opset 17", "Opset 18"])
        self.form_layout.addRow("   ONNX Opset:", self.cb_onnx) # Indented visually

        self.cb_tensorrt = QComboBox()
        self.cb_tensorrt.addItems(["FP16", "FP32", "INT8"])
        self.form_layout.addRow("   TensorRT Optimization:", self.cb_tensorrt)

        # 5. Always show log panel
        self.form_layout.addRow("Always show log panel:", ToggleSwitch())

        # 6. Dev Mode
        self.form_layout.addRow("Dev Mode:", ToggleSwitch())

        # --- Adding 10 Random Settings to force scrollbar ---
        separator_rand = QLabel("<b>Extended Settings:</b>")
        separator_rand.setStyleSheet("margin-top: 10px;")
        self.form_layout.addRow(separator_rand)

        for i in range(1, 11):
            label_text = f"Random Parameter #{i}:"
            if random.choice([True, False]):
                widget = ToggleSwitch()
            else:
                widget = QComboBox()
                widget.addItems(["Low", "Medium", "High"])
            self.form_layout.addRow(label_text, widget)

        # Set widget to scroll area
        self.scroll_area.setWidget(self.settings_widget)
        v_layout.addWidget(self.scroll_area)

        # Separator
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)
        v_layout.addWidget(line2)

        # --- Footer Buttons ---
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(10, 10, 10, 10)

        # Restore Default (Bottom Left)
        self.btn_restore = QPushButton("Restore to default")
        # Styling it slightly differently to indicate it's not a primary action
        self.btn_restore.setStyleSheet("color: #c0392b;")
        self.btn_restore.clicked.connect(self.restore_defaults)

        self.btn_cancel = QPushButton("Cancel")
        self.btn_ok = QPushButton("OK")
        self.btn_ok.setDefault(True)

        self.btn_cancel.clicked.connect(self.reject)
        self.btn_ok.clicked.connect(self.accept)

        btn_layout.addWidget(self.btn_restore)
        btn_layout.addStretch() # Spacer
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_ok)

        v_layout.addLayout(btn_layout)

    def showEvent(self, event):
        """
        Overriding showEvent to calculate geometry dynamically
        based on parent size and content size.
        """
        super().showEvent(event)

        if not self.parent():
            return

        parent_rect = self.parent().geometry()
        parent_center = parent_rect.center()

        # Calculate desired width (fixed or percentage)
        width = 500

        # Calculate desired height
        # We let the layout calculate the hint, but clamp it
        # Note: We ensure the dialog is not taller than Parent - 50px
        max_height = parent_rect.height() - 50

        # Get the size hint of the dialog content
        hint_height = self.layout().sizeHint().height()

        # If content is smaller than max, use content size. Otherwise use max.
        # We set a minimum height just in case (e.g., 300)
        actual_height = min(max(hint_height, 300), max_height)

        self.resize(width, actual_height)

        # Center the dialog
        geo = self.frameGeometry()
        geo.moveCenter(parent_center)
        self.move(geo.topLeft())

    def restore_defaults(self):
        print("Restoring defaults logic goes here...")

# --- Main Window for Demo ---

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Application Window")
        self.resize(1000, 800) # Large enough to test resizing logic

        # Central widget
        central = QWidget()
        layout = QVBoxLayout(central)

        info_lbl = QLabel("Main Window.\nResize me and click Settings to test dialog constraint.")
        info_lbl.setAlignment(Qt.AlignCenter)

        btn = QPushButton("Open Settings Dialog")
        btn.setFixedSize(200, 50)
        btn.clicked.connect(self.open_settings)

        layout.addStretch()
        layout.addWidget(info_lbl)
        layout.addWidget(btn, 0, Qt.AlignCenter)
        layout.addStretch()

        self.setCentralWidget(central)

    def open_settings(self):
        dlg = FramelessSettingsDialog(self)
        # exec() blocks the interaction with main window,
        # but still allows minimizing the group via the taskbar if OS supports it.
        dlg.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
