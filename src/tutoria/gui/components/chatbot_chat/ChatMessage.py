import math
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QTextDocument
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from tutoria.gui.components.chatbot_chat.BubbleFrame import BubbleFrame
from tutoria.gui.components.chatbot_chat.Bubbletext import BubbleText
from tutoria.gui.components.chatbot_chat.CircleAvatar import CircleAvatar

AVATAR_SIZE = 48
MAX_BUBBLE_WIDTH = 720
BUBBLE_WIDTH_RATIO = 0.85
MIN_BUBBLE_WIDTH = 60


class ChatMessage(QWidget):
    def __init__(
        self,
        text: str,
        icon_path: str | Path,
        side: str,
        bubble_bg: str,
        bubble_border: str,
        avatar_bg: str,
        text_object_name: str,
        icon_ratio: float = 0.75,
        avatar_fill: bool = False,
        markdown: bool = True,
        parent=None,
    ):
        super().__init__(parent)
        self._text = ""
        self._markdown = markdown

        self.avatar = CircleAvatar(
            icon_path,
            size=AVATAR_SIZE,
            bg_color=avatar_bg,
            icon_ratio=icon_ratio,
            fill=avatar_fill,
        )

        self.bubble = BubbleFrame(
            tail_side=side,
            bg_color=bubble_bg,
            border_color=bubble_border,
            tail_y=AVATAR_SIZE // 2,
        )

        self.text_view = BubbleText(text_object_name, markdown=markdown)

        bubble_layout = QVBoxLayout(self.bubble)
        bubble_layout.setContentsMargins(*self.bubble.content_margins())
        bubble_layout.addWidget(self.text_view)

        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(6)
        if side == "left":
            row.addWidget(self.avatar, alignment=Qt.AlignTop)
            row.addWidget(self.bubble, 100)
            row.addStretch(1)
        else:
            row.addStretch(1)
            row.addWidget(self.bubble, 100)
            row.addWidget(self.avatar, alignment=Qt.AlignTop)

        self.set_text(text)

    def set_text(self, text: str):
        self._text = text
        self.text_view.set_content(text)
        self._update_bubble_width()

    def _update_bubble_width(self):
        left, _, right, _ = self.bubble.content_margins()
        limit = int(self.width() * BUBBLE_WIDTH_RATIO)
        limit = max(MIN_BUBBLE_WIDTH, min(limit, MAX_BUBBLE_WIDTH))

        doc = QTextDocument()
        doc.setDefaultFont(self.text_view.font())
        doc.setDocumentMargin(0)
        if self._markdown:
            doc.setMarkdown(self._text)
        else:
            doc.setPlainText(self._text)
        doc.setTextWidth(-1)
        ideal = math.ceil(doc.idealWidth()) + 2 + left + right

        self.bubble.setMaximumWidth(max(MIN_BUBBLE_WIDTH, min(limit, ideal)))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_bubble_width()