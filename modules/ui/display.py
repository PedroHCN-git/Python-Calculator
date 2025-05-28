from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt
from modules.configs import BIG_TEXT, TEXT_MARGIN, MINIMUM_WIDTH


class Display(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyleSheet()
        self.setMinimumHeight(BIG_TEXT * 2)
        self.setMinimumWidth(MINIMUM_WIDTH)
        self.setTextMargins(*[TEXT_MARGIN for _ in range(4)])
        self.setAlignment(Qt.AlignmentFlag.AlignRight)

    def configStyleSheet(self):
        self.setStyleSheet(f'font-size: {BIG_TEXT}px;')
