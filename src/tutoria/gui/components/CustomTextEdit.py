from PySide6.QtWidgets import QTextEdit

class CustomTextEdit(QTextEdit):
    def __init__(self,text):
        super().__init__()

        self.setPlaceholderText(text)
        self.setDisabled(True)