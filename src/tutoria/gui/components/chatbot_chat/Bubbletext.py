import math

from PySide6.QtCore import Qt
from PySide6.QtGui import QTextBlockFormat, QTextCursor, QTextOption
from PySide6.QtWidgets import QFrame, QSizePolicy, QTextBrowser


class BubbleText(QTextBrowser):
    def __init__(self, object_name: str, markdown: bool = True, parent=None):
        super().__init__(parent)
        self._markdown = markdown

        self.setObjectName(object_name)
        self.setFrameShape(QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        self.setOpenExternalLinks(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumWidth(1)

        self.document().setDocumentMargin(0)
        self.document().documentLayout().documentSizeChanged.connect(self._fit_height)

    def set_content(self, text: str):
        if self._markdown:
            self.setMarkdown(text)
        else:
            self.setPlainText(text)

        cursor = QTextCursor(self.document())
        cursor.select(QTextCursor.Document)
        block_format = QTextBlockFormat()
        block_format.setNonBreakableLines(False)
        cursor.mergeBlockFormat(block_format)

    def _fit_height(self, size):
        self.setFixedHeight(math.ceil(size.height()) + 2)