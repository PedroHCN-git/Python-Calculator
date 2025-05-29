from PySide6.QtWidgets import QPushButton, QWidget, QGridLayout
from modules.configs import MEDIUM_TEXT
from modules.utils import isNumOrDot, isEmpty, isValidNum
from PySide6.QtCore import Slot
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from display import Display
    from info import Info


class Button(QPushButton):
    def __init__(self, text: str, parent: QWidget | None = None):
        super().__init__(text, parent)
        self.configStyle()

    def configStyle(self):
        fonte = self.font()
        fonte.setPixelSize(MEDIUM_TEXT)
        self.setFont(fonte)
        self.setMinimumSize(75, 75)


class ButtonsGrid(QGridLayout):
    def __init__(
            self, display: 'Display', info: 'Info', *args, **kwargs
            ) -> None:
        super().__init__(*args, **kwargs)
        self.display = display
        self.info = info
        self._equation = ''

        self._gridMask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['',  '0', '.', '='],
        ]

        self._rigth = None
        self._left = None
        self._op = None

        for line, list in enumerate(self._gridMask):
            for index, value in enumerate(list):
                button = Button(value)
                if not isNumOrDot(value) and not isEmpty(value):
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButton(button)
                self.addWidget(button, line, index)
                slot = self._makeSlot(self._insertText, button)
                self._connectButtonClicked(button, slot)

    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self, button):
        text = button.text()
        print('texto do botão especial:', text)

        if text == 'C':
            self._connectButtonClicked(button, self._clear)

        if text in '+-/*':
            self._connectButtonClicked(
                button,
                self._makeSlot(self._operatorClicked, button)
            )

        if text == "=":
            self._connectButtonClicked(button, self._eq)

    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot():
            func(*args, **kwargs)
        return realSlot

    def _insertText(self, button):
        buttonText = button.text()
        newDisplayText = self.display.text() + buttonText

        if not isValidNum(newDisplayText):
            return

        self.display.insert(buttonText)

    def _clear(self):
        self._left = None
        self._rigth = None
        self._op = None
        self.equation = ''
        self.display.clear()

    def _operatorClicked(self, button):
        buttonText = button.text()
        displayText = self.display.text()

        if not isValidNum(displayText) and self._left is None:
            print('não existe valor para operar')
            return

        if self._left is None:
            self._left = float(displayText)

        self.display.clear()

        self._op = buttonText
        self.equation = f"{self._left} {self._op}"

    def _eq(self):
        displayText = self.display.text()

        if not isValidNum(displayText):
            print('sem nada a direita')
            return

        if self._rigth is None and self._left is not None:
            self._rigth = float(displayText)
        else:
            print('não é possível operar com nada')
            return

        self.equation += f" {self._rigth}"
        self.display.clear()

        try:
            result = eval(self.equation)
            self.display.setText(str(result))
        except ZeroDivisionError:
            self.equation = 'impossível divisão por zero!'
            self._left = None
            self._rigth = None
            self._op = None
            return

        self._left = result
        self._rigth = None
        self._op = None
        self.equation = ''
