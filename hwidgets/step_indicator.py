from pprint import pprint
from string import Template
from typing import Literal

from .utils import load_qss
from .styles import (
    FontConfig,
    Theme,
    StepIndicatorStyle,
)
from PySide6.QtCore import (
    QSize,
    Qt,
)
from PySide6.QtGui import (
    QPixmap,
    Qt,
    QFontMetrics,
    QFont,
    QPainter,
)
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
)
from .hstyle import (
    DEBUG_GEOMETRY,
    draw_widget_rect,
)


class HStep(QLabel):

    def __init__(
        self,
        /,
        parent: QWidget | None = None,
        f: Qt.WindowType = None,
        *,
        style: StepIndicatorStyle,
        no: int,
        name: str,
        textFormat: Qt.TextFormat | None = None,
        pixmap: QPixmap | None = None,
        scaledContents: bool | None = None,
        alignment: Qt.AlignmentFlag | None = None,
        wordWrap: bool | None = None,
        margin: int | None = None,
        indent: int | None = None,
        openExternalLinks: bool | None = None,
        textInteractionFlags: Qt.TextInteractionFlag | None = None,
        hasSelectedText: bool | None = None,
        selectedText: str | None = None,
    ) -> None:
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self._step_text = f"{no}. {name}"
        self.setText(self._step_text)
        self.step_style = style
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding,
        )
        self.fonts: dict[str, QFont] = {
            'completed': self.step_style.font_completed.make_font(),
            'current': self.step_style.font_current.make_font(),
            'upcoming': self.step_style.font_upcoming.make_font(),
        }
        self._update_stylesheet()
        self._calculate_minimum_size()
        self.setState('upcoming')


    def _calculate_minimum_size(self) -> None:
        """Calculate minimum size needed to display the full text"""
        font_metrics = QFontMetrics(self.fonts['current'])
        content_width = font_metrics.horizontalAdvance(self._step_text)
        self.setFixedWidth(content_width)


    def update_style(self):
        style = self.style()
        style.unpolish(self)
        style.polish(self)
        # Force geometry recalculation
        self.updateGeometry()
        self.update()


    def _update_stylesheet(self) -> None:
        step_style = self.step_style

        qss_template = Template(load_qss("step.qss"))
        qss = qss_template.substitute(
            font_completed_color=f"{step_style.font_completed_color}",
            font_current_color=f"{step_style.font_current_color}",
            font_upcoming_color=f"{step_style.font_upcoming_color}",
        )
        self.setStyleSheet(qss)


    def setState(self, state: Literal['completed', 'current', 'upcoming']) -> None:
        font = self.fonts.get(state, self.fonts['upcoming'])
        self.setFont(font)
        self.setProperty("state", state)
        self.update_style()


    def paintEvent(self, event):
        if DEBUG_GEOMETRY:
            painter = QPainter(self)
            draw_widget_rect(self, painter)
            painter.end()

        return super().paintEvent(event)



class HStepIndicator(QWidget):
    def __init__(
        self,
        parent,
        theme: type[Theme]
    ):
        super().__init__(parent)
        self._steps: list[HStep] = []
        self.step_style = theme.step_indicator
        self.current_step: int = 0

        self.step_layout = QHBoxLayout(self)
        self.step_layout.setContentsMargins(0, 0, 0, 0)
        self.step_layout.setSpacing(self.step_style.spacing)

        self.setFixedHeight(self.step_style.height)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)


    def sizeHint(self):
        """Preferred size: sum of all step widths plus spacing"""
        w: int = sum(s.width() for s in self._steps)
        if len(self._steps) > 1:
            w += (len(self._steps) - 1) * self.step_layout.spacing()
        return QSize(w, self.height())


    def minimumSizeHint(self):
        """Minimum size: sum of all step widths plus spacing"""
        w: int = sum(s.width() for s in self._steps)
        if len(self._steps) > 1:
            w += (len(self._steps) - 1) * self.step_layout.spacing()
        return QSize(w, self.height())


    def _update_fixed_width(self) -> None:
        """Calculate and set the fixed width based on all steps"""
        total_width = sum(step.width() for step in self._steps)
        if len(self._steps) > 1:
            total_width += (len(self._steps) - 1) * self.step_layout.spacing()
        self.setFixedWidth(total_width)


    def setSteps(self, names: list[str]) -> None:
        for name in names:
            self._append_step(name)
            self.adjustSize()
        self._update_fixed_width()


    def _append_step(self, name: str) -> None:
        step: HStep = HStep(
            no=len(self._steps), name=name, style=self.step_style
        )
        self._steps.append(step)
        self.step_layout.addWidget(step)


    def resetStep(self) -> None:
        self.current_step = 0
        for step in self._steps:
            step.setState('upcoming')


    def setCurrentStep(self, no: int) -> None:
        self.current_step = no
        for step in self._steps[:no]:
            step.setState('completed')
        for step in self._steps[no+1:]:
            step.setState('upcoming')
        self._steps[no].setState('current')


    def nextStep(self) -> None:
        self._steps[self.current_step].setState('completed')
        self.current_step += 1
        self._steps[self.current_step].setState('current')


    def previousStep(self) -> None:
        self._steps[self.current_step].setState('upcoming')
        self.current_step -= 1
        self._steps[self.current_step].setState('current')
