
from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QLabel,
    QGridLayout
)


class RandomAnimatorGenerator(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Random Animator Generator")
        self.setMinimumWidth(400)
        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout(self)

        # Grid layout
        grid_layout = QGridLayout()

        # Animation Timing
        grid_layout.addWidget(QLabel("Animation Timing"),0,0)



        self.create_button = QPushButton("Create")

        layout.addLayout(grid_layout)
        layout.addWidget(self.create_button)