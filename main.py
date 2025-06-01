import sys
from PySide6.QtWidgets import QApplication
from modules.ui import (
    MainWindow,
    Info,
    Display,
    ButtonsGrid
)
from PySide6.QtGui import QIcon
from modules.configs import ICON_PATH
from modules.configs import setup_theme

if __name__ == '__main__':
    app = QApplication(sys.argv)
    setup_theme(app)
    window = MainWindow()
    icon = QIcon(str(ICON_PATH))
    app.setWindowIcon(icon)

    # info
    info = Info('')
    window.addWigetToVLayout(info)

    # display
    display = Display()
    window.addWigetToVLayout(display)

    buttonsGrid = ButtonsGrid(display, info, window)
    window.vLayout.addLayout(buttonsGrid)

    # janela principal
    window.adjustFixedSize()
    window.show()

    app.exec()
