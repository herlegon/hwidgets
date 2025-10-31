import sys
import vlc
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QSlider, QFileDialog
from PySide6.QtCore import Qt, QTimer
import sys
import vlc
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QSlider, QFileDialog, QLabel, QHBoxLayout
)
from PySide6.QtCore import Qt, QTimer, QTime

class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Embedded VLC Player")
        self.setGeometry(100, 100, 900, 600)

        # Central widget
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout(self.widget)

        # Video frame
        self.videoframe = QWidget(self)
        self.videoframe.setStyleSheet("background: black;")
        # Ensures VLC renders inside our widget
        # self.videoframe.setAttribute(Qt.WA_OpaquePaintEvent, True)
        # self.videoframe.setAttribute(Qt.WA_NoSystemBackground, True)
        # self.videoframe.setAttribute(Qt.WA_PaintOnScreen, True)
        self.layout.addWidget(self.videoframe)

        # Slider and time label
        slider_layout = QHBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 1000)
        self.slider.sliderMoved.connect(self.set_position)
        slider_layout.addWidget(self.slider)

        self.time_label = QLabel("00:00 / 00:00")
        slider_layout.addWidget(self.time_label)
        self.layout.addLayout(slider_layout)

        # Control buttons
        btn_layout = QHBoxLayout()
        self.open_button = QPushButton("Open Video")
        self.open_button.clicked.connect(self.open_file)
        btn_layout.addWidget(self.open_button)

        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play_pause)
        btn_layout.addWidget(self.play_button)

        self.layout.addLayout(btn_layout)

        # VLC player
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        # Timer for slider and time updates
        self.timer = QTimer(self)
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.update_ui)
        self.timer.start()

    def showEvent(self, event):
        """Set VLC video output AFTER widget is shown"""
        super().showEvent(event)
        if sys.platform.startswith("linux"):
            self.player.set_xwindow(self.videoframe.winId())
        elif sys.platform == "win32":
            self.player.set_hwnd(self.videoframe.winId())
        elif sys.platform == "darwin":
            self.player.set_nsobject(int(self.videoframe.winId()))

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")
        if filename:
            media = self.instance.media_new(filename)
            self.player.set_media(media)
            self.play_pause()

    def play_pause(self):
        if self.player.is_playing():
            self.player.pause()
            self.play_button.setText("Play")
        else:
            self.player.play()
            self.play_button.setText("Pause")

    def set_position(self, position):
        """Slider moved by user"""
        self.player.set_position(position / 1000.0)

    def update_ui(self):
        """Update slider and time label"""
        if self.player is None:
            return

        # Update slider
        if self.player.is_playing():
            pos = int(self.player.get_position() * 1000)
            self.slider.setValue(pos)

        # Update time
        length_ms = self.player.get_length()
        current_ms = self.player.get_time()
        if length_ms > 0:
            total_time = QTime(0,0,0).addMSecs(length_ms)
            current_time = QTime(0,0,0).addMSecs(current_ms)
            self.time_label.setText(f"{current_time.toString('mm:ss')} / {total_time.toString('mm:ss')}")
        else:
            self.time_label.setText("00:00 / 00:00")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec())
