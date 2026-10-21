from PySide6.QtWidgets import QTextEdit

class ChatBotChat(QTextEdit):
    def __int__(self):
        super().__init__()
        self.setText("ChatBot")