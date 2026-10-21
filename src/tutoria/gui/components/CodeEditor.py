from PySide6.QtWidgets import QTextEdit

class CodeEditor(QTextEdit):
    def __init__(self):
        super().__init__()

        self.setPlaceholderText("Descripción del problema")