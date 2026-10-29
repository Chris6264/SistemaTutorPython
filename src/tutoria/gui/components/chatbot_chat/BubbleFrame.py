from PySide6.QtCore import QRectF
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QWidget


class BubbleFrame(QWidget):
    TAIL_W = 8
    RADIUS = 14

    def __init__(
        self,
        tail_side: str = "left",
        bg_color: str = "#f1f5f9",
        border_color: str = "#cbd5e1",
        tail_y: int = 18,
        parent=None,
    ):
        super().__init__(parent)
        self.tail_side = tail_side
        self.tail_y = tail_y
        self.bg_color = QColor(bg_color)
        self.border_color = QColor(border_color)

    def content_margins(self, pad_x: int = 16, pad_y: int = 12):
        extra = self.TAIL_W
        if self.tail_side == "left":
            return pad_x + extra, pad_y, pad_x, pad_y
        return pad_x, pad_y, pad_x + extra, pad_y

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        if self.tail_side == "left":
            body = QRectF(self.TAIL_W + 0.5, 0.5, w - self.TAIL_W - 1, h - 1)
        else:
            body = QRectF(0.5, 0.5, w - self.TAIL_W - 1, h - 1)

        path = QPainterPath()
        path.addRoundedRect(body, self.RADIUS, self.RADIUS)

        y = self.tail_y
        tail = QPainterPath()
        if self.tail_side == "left":
            tail.moveTo(body.left() + 1, y - 6)
            tail.lineTo(0.5, y)
            tail.lineTo(body.left() + 1, y + 6)
        else:
            tail.moveTo(body.right() - 1, y - 6)
            tail.lineTo(w - 0.5, y)
            tail.lineTo(body.right() - 1, y + 6)
        tail.closeSubpath()

        painter.setPen(QPen(self.border_color, 1))
        painter.setBrush(self.bg_color)
        painter.drawPath(path.united(tail))