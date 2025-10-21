

from dataclasses import dataclass
from PySide6.QtCore import (
    Qt,
)
from ..title_bar.title_bar import TitleBar


@dataclass
class RlgWindowBase:
    _moving: bool = False
    _resizing: bool = False
    _resizable: bool = True
    _previous_window_state: Qt.WindowState = Qt.WindowState.WindowNoState
    _titlebar: TitleBar | None = None

    @property
    def moving(self) -> bool:
        return self._moving

    @moving.setter
    def moving(self, enabled: bool) -> None:
        self._moving = enabled


    @property
    def resizable(self) -> bool:
        return self._resizable

    @resizable.setter
    def resizable(self, enabled: bool) -> None:
        self._resizable = enabled


    @property
    def resizing(self) -> bool:
        return self._resizing

    @resizing.setter
    def resizing(self, enabled: bool) -> None:
        self._resizing = enabled


    @property
    def previous_window_state(self) -> bool:
        return self._previous_window_state

    @previous_window_state.setter
    def previous_window_state(self, enabled: bool) -> None:
        self._previous_window_state = enabled


    @property
    def titlebar(self) -> TitleBar:
        return self._titlebar

    @titlebar.setter
    def titlebar(self, bar: TitleBar) -> None:
        self._titlebar = bar
