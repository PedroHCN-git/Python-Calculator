from PySide6.QtWidgets import QLabel, QWidget
from PySide6.QtCore import Qt
from modules.configs import SMAL_TEXT


class Info(QLabel):
    def __init__(self, text: str, parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.configStyleSheet()

    def configStyleSheet(self):
        self.setStyleSheet(f'font-size: {SMAL_TEXT}')
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
