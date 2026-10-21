from PySide6.QtWidgets import QPlainTextEdit

class CodeEditor(QPlainTextEdit):
    def __init__(self,text):
        super().__init__()

        self.setPlaceholderText(text)