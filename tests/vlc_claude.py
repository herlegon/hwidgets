import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QPushButton, QSlider, QLabel, QFileDialog,
                               QStyle, QFrame)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPalette, QColor

try:
    import vlc
except ImportError:
    print("Error: python-vlc is not installed.")
    print("Install it with: pip install python-vlc")
    sys.exit(1)
class VLCPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VLC Media Player")
        self.setGeometry(100, 100, 1000, 600)

        # Create VLC instance with options to disable decorations and suppress errors
        vlc_args = [
            '--no-video-title-show',  # Don't show video title
            '--no-video-on-top',      # Don't keep on top
            '--quiet',                # Suppress console output
            '--no-stats',             # Don't collect stats
            '--avcodec-hw=any',       # Enable hardware acceleration
            '--clock-jitter=0',       # Reduce clock jitter
            '--clock-synchro=0',      # Disable clock synchronization issues
        ]

        if sys.platform.startswith('linux'):
            vlc_args.append('--no-xlib')

        self.instance = vlc.Instance(vlc_args)
        self.player = self.instance.media_player_new()

        # Track if user is dragging slider
        self.is_slider_pressed = False
        self.media_loaded = False

        self.init_ui()

        # Timer to update slider position
        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_ui)
        self.timer.start()

    def init_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 5)
        main_widget.setLayout(layout)

        # Video frame
        self.video_frame = QFrame()
        self.video_frame.setStyleSheet("background-color: black;")
        self.video_frame.setMinimumSize(640, 360)
        layout.addWidget(self.video_frame, stretch=1)

        # Controls layout
        controls_layout = QVBoxLayout()
        controls_layout.setContentsMargins(10, 5, 10, 5)

        # Time slider
        slider_layout = QHBoxLayout()
        self.time_label = QLabel("00:00")
        self.time_label.setMinimumWidth(50)
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setMaximum(1000)
        self.position_slider.sliderPressed.connect(self.on_slider_pressed)
        self.position_slider.sliderReleased.connect(self.on_slider_released)
        self.position_slider.sliderMoved.connect(self.on_slider_moved)
        self.duration_label = QLabel("00:00")
        self.duration_label.setMinimumWidth(50)

        slider_layout.addWidget(self.time_label)
        slider_layout.addWidget(self.position_slider)
        slider_layout.addWidget(self.duration_label)
        controls_layout.addLayout(slider_layout)

        # Buttons layout
        buttons_layout = QHBoxLayout()

        # Open file button
        self.open_btn = QPushButton("Open File")
        self.open_btn.clicked.connect(self.open_file)

        # Play button
        self.play_btn = QPushButton()
        self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_btn.clicked.connect(self.play_pause)
        self.play_btn.setEnabled(False)

        # Stop button
        self.stop_btn = QPushButton()
        self.stop_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stop_btn.clicked.connect(self.stop)
        self.stop_btn.setEnabled(False)

        # Volume slider
        volume_label = QLabel("Volume:")
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(100)
        self.volume_slider.setMaximumWidth(100)
        self.volume_slider.valueChanged.connect(self.set_volume)

        buttons_layout.addWidget(self.open_btn)
        buttons_layout.addWidget(self.play_btn)
        buttons_layout.addWidget(self.stop_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(volume_label)
        buttons_layout.addWidget(self.volume_slider)

        controls_layout.addLayout(buttons_layout)
        layout.addLayout(controls_layout)

    def showEvent(self, event):
        super().showEvent(event)
        # Embed VLC player after the widget is shown
        if sys.platform.startswith('linux'):
            self.player.set_xwindow(int(self.video_frame.winId()))
        elif sys.platform == "win32":
            self.player.set_hwnd(int(self.video_frame.winId()))
        elif sys.platform == "darwin":
            self.player.set_nsobject(int(self.video_frame.winId()))

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Video File",
            "",
            "Video Files (*.mp4 *.mkv *.avi *.webm *.mov *.flv *.wmv);;All Files (*.*)"
        )

        if file_name:
            media = self.instance.media_new(file_name)
            self.player.set_media(media)
            self.media_loaded = True
            self.play_btn.setEnabled(True)
            self.stop_btn.setEnabled(True)

            # Parse the media to get duration
            media.parse()

            # Start playing
            if self.player.play() == -1:
                print("Error: Unable to play media")
            else:
                self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

    def play_pause(self):
        if not self.media_loaded:
            return

        if self.player.is_playing():
            self.player.pause()
            self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            if self.player.play() == -1:
                print("Error: Unable to play media")
            else:
                self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

    def stop(self):
        if not self.media_loaded:
            return

        self.player.stop()
        self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.position_slider.setValue(0)
        self.time_label.setText("00:00")

    def set_volume(self, volume):
        self.player.audio_set_volume(volume)

    def on_slider_pressed(self):
        self.is_slider_pressed = True

    def on_slider_moved(self, position):
        # Update time label while dragging
        if self.media_loaded:
            total_time = self.player.get_length()
            if total_time > 0:
                new_time = int((position / 1000.0) * total_time)
                self.time_label.setText(self.format_time(new_time))

    def on_slider_released(self):
        self.is_slider_pressed = False
        if self.media_loaded:
            position = self.position_slider.value()
            self.player.set_position(position / 1000.0)

    def update_ui(self):
        if not self.media_loaded:
            return

        # Update slider position if not being dragged
        if not self.is_slider_pressed:
            media_pos = self.player.get_position()
            if media_pos >= 0:
                self.position_slider.setValue(int(media_pos * 1000))

        # Update time labels
        current_time = self.player.get_time()
        total_time = self.player.get_length()

        if current_time >= 0 and not self.is_slider_pressed:
            self.time_label.setText(self.format_time(current_time))

        if total_time >= 0:
            self.duration_label.setText(self.format_time(total_time))

        # Update play button icon based on state
        if self.player.is_playing():
            self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    @staticmethod
    def format_time(ms):
        if ms < 0:
            return "00:00"
        seconds = ms // 1000
        mins = seconds // 60
        secs = seconds % 60
        hours = mins // 60
        mins = mins % 60

        if hours > 0:
            return f"{hours:02d}:{mins:02d}:{secs:02d}"
        return f"{mins:02d}:{secs:02d}"

    def closeEvent(self, event):
        self.player.stop()
        self.timer.stop()
        event.accept()


def main():
    app = QApplication(sys.argv)
    player = VLCPlayer()
    player.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
