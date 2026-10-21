from PySide6.QtWidgets import QLineEdit

class CustomCounter(QLineEdit):
    def __init__(self,text):
        super().__init__()
        self.setDisabled(True)
        self.setText(text)