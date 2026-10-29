from pathlib import Path

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPixmap
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QWidget


class CircleAvatar(QWidget):
    def __init__(
        self,
        icon_path: str | Path,
        size: int = 36,
        bg_color: str = "#000000",
        icon_ratio: float = 0.56,
        fill: bool = False,
        parent=None,
    ):
        super().__init__(parent)
        self.setFixedSize(size, size)
        self.bg_color = QColor(bg_color)
        self.icon_ratio = icon_ratio
        self.fill = fill

        self.renderer = None
        self.pixmap = None
        if Path(icon_path).suffix.lower() == ".svg":
            self.renderer = QSvgRenderer(str(icon_path))
        else:
            self.pixmap = QPixmap(str(icon_path))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        painter.setPen(Qt.NoPen)
        painter.setBrush(self.bg_color)
        painter.drawEllipse(self.rect())

        if self.renderer is not None:
            self._paint_svg(painter)
        elif self.pixmap is not None and not self.pixmap.isNull():
            self._paint_pixmap(painter)

    def _paint_svg(self, painter: QPainter):
        if not self.renderer.isValid():
            return
        side = self.width() * self.icon_ratio
        offset = (self.width() - side) / 2
        self.renderer.render(painter, QRectF(offset, offset, side, side))

    def _paint_pixmap(self, painter: QPainter):
        dpr = self.devicePixelRatioF()
        w = self.width()

        if self.fill:
            side = w
            mode = Qt.AspectRatioMode.KeepAspectRatioByExpanding
            clip = QPainterPath()
            clip.addEllipse(QRectF(0, 0, w, w))
            painter.setClipPath(clip)
        else:
            side = w * self.icon_ratio
            mode = Qt.AspectRatioMode.KeepAspectRatio

        scaled = self.pixmap.scaled(
            int(side * dpr), int(side * dpr), mode, Qt.TransformationMode.SmoothTransformation
        )
        scaled.setDevicePixelRatio(dpr)
        x = (w - scaled.width() / dpr) / 2
        y = (w - scaled.height() / dpr) / 2
        painter.drawPixmap(QPointF(x, y), scaled)