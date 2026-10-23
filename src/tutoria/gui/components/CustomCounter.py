from PySide6.QtWidgets import QLineEdit

class CustomCounter(QLineEdit):
    def __init__(self,text, counter):
        super().__init__()
        self.setDisabled(True)
        self.setText(f"{text}: {counter}")
        self.setFixedWidth(200)