from PySide6.QtWidgets import QPushButton

class CustomButton(QPushButton):
    def __init__(self,text):
        super().__init__()
        self.setText(text)