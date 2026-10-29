from PySide6.QtWidgets import QLineEdit

class CustomCounter(QLineEdit):
    def __init__(self,text):
        super().__init__()
        self.label = text
        self.counter = 0
        self.setDisabled(True)
        self.setText(f"{text}:              {self.counter}")
        self.setFixedWidth(200)

    def set_counter(self, new_counter):
        self.counter = new_counter
        self.setText(f"{self.label}:              {self.counter}")

    def get_counter(self) -> int:
        return self.counter