from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import QScrollArea, QVBoxLayout, QWidget

from tutoria.gui.components.chatbot_chat.BotMessage import BotMessage
from tutoria.gui.components.chatbot_chat.ChatInput import ChatInput
from tutoria.gui.components.chatbot_chat.ChatMessage import ChatMessage
from tutoria.gui.components.chatbot_chat.UserMessage import UserMessage


class ChatBotChat(QWidget):
    message_sent = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("ChatScroll")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.content = QWidget()
        self.content.setObjectName("ChatContent")

        self.messages_layout = QVBoxLayout(self.content)
        self.messages_layout.setContentsMargins(8, 8, 8, 8)
        self.messages_layout.setSpacing(12)
        self.messages_layout.addStretch(1)

        self.scroll_area.setWidget(self.content)

        self.chat_input = ChatInput()
        self.chat_input.submitted.connect(self._on_submitted)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(8)
        root.addWidget(self.scroll_area, 1)
        root.addWidget(self.chat_input)
        self.setMinimumHeight(260)

    def showEvent(self, event):
        super().showEvent(event)
        self.chat_input.focus_input()

    def _on_submitted(self, text: str):
        self.add_user_message(text)
        self.message_sent.emit(text)

    def set_busy(self, busy: bool):
        self.chat_input.set_busy(busy)

    def add_bot_message(self, text: str) -> BotMessage:
        return self._add_message(BotMessage(text))

    def add_user_message(self, text: str) -> UserMessage:
        return self._add_message(UserMessage(text))

    def _add_message(self, message: ChatMessage):
        self.messages_layout.insertWidget(self.messages_layout.count() - 1, message)
        QTimer.singleShot(0, self._scroll_to_bottom)
        return message

    def _scroll_to_bottom(self):
        bar = self.scroll_area.verticalScrollBar()
        bar.setValue(bar.maximum())

    def scroll_to_bottom(self):
        self._scroll_to_bottom()

    def clear_messages(self):
        while self.messages_layout.count() > 1:
            item = self.messages_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()