import sys
import os

# Add the current directory to sys.path to ensure hwidgets can be imported
sys.path.append(os.getcwd())

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSizePolicy
from hwidgets.step_indicator import HStepIndicator
from hwidgets.styles import Theme

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout(window)

    theme = Theme()
    step_indicator = HStepIndicator(window, theme)
    step_indicator.setSteps(["Step 1", "Step 2: Long Label", "Step 3: Very Long Label That Should Not Shrink"])
    step_indicator.setCurrentStep(1)

    layout.addWidget(step_indicator)

    # Set a small width to force shrinking if it happens
    window.resize(300, 100)

    print(f"StepIndicator SizeHint: {step_indicator.sizeHint()}")
    print(f"StepIndicator MinimumSizeHint: {step_indicator.minimumSizeHint()}")
    print(f"StepIndicator Horizontal Policy: {step_indicator.sizePolicy().horizontalPolicy()}")

    # Check font weight of the current step (index 1)
    current_step_widget = step_indicator._steps[1]
    print(f"Current Step Font Weight: {current_step_widget.font().weight()}")
    print(f"Current Step Style Sheet: {current_step_widget.styleSheet()}")

    window.show()

    print("Running reproduction script. Close the window to finish.")
    sys.exit(app.exec())
