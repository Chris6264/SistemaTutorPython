import sys
from PySide6.QtWidgets import QApplication
from tutoria.gui.components.MainWindow import MainWindow

class VentanaPrincipal:
    def __init__(self):
        app = QApplication(sys.argv)

        window = MainWindow()
        window.show()

        app.exec()