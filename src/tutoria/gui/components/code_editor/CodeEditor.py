from PySide6.QtWidgets import QPlainTextEdit, QTextEdit
from PySide6.QtGui import QColor, QPainter, QTextFormat
from PySide6.QtCore import QEvent, QRect, Qt
from tutoria.gui.components.code_editor.LineNumberArea import LineNumberArea

class CodeEditor(QPlainTextEdit):
    def __init__(self,parent = None):
        super().__init__()
        self.setPlaceholderText("Editor De Codigo")
        self.setLineWrapMode(QPlainTextEdit.NoWrap)

        self.gutter_bg = QColor("#fdfeff")
        self.gutter_fg = QColor("#a0a7b4")
        self.gutter_fg_current = QColor("#0f172a")
        self.current_line_bg = QColor("#f1f5f9")

        self.line_number_area = LineNumberArea(self)

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        self.ensurePolished()
        self._on_font_changed()
        self.highlight_current_line()

    def line_number_area_width(self):
        digits = len(str(max(1, self.blockCount())))
        return 16 + self.fontMetrics().horizontalAdvance("9") * max(digits, 2)

    def update_line_number_area_width(self, _=None):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def _on_font_changed(self):
        self.setTabStopDistance(self.fontMetrics().horizontalAdvance(" ") * 4)
        self.update_line_number_area_width()
        self.line_number_area.update()

    def changeEvent(self, event):
        super().changeEvent(event)
        if not hasattr(self, "line_number_area"):
            return               
        if event.type() in (QEvent.FontChange, QEvent.StyleChange):
            self._on_font_changed()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(
            QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height())
        )

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(
                0, rect.y(), self.line_number_area.width(), rect.height()
            )
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width()

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.setFont(self.font())
        painter.fillRect(event.rect(), self.gutter_bg)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = round(
            self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        )
        bottom = top + round(self.blockBoundingRect(block).height())
        current = self.textCursor().blockNumber()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                painter.setPen(
                    self.gutter_fg_current if block_number == current else self.gutter_fg
                )
                painter.drawText(
                    0, top,
                    self.line_number_area.width() - 8,
                    self.fontMetrics().height(),
                    Qt.AlignRight,
                    str(block_number + 1),
                )
            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            block_number += 1

    def highlight_current_line(self):
        extra = []
        if not self.isReadOnly():
            sel = QTextEdit.ExtraSelection()
            sel.format.setBackground(self.current_line_bg)
            sel.format.setProperty(QTextFormat.FullWidthSelection, True)
            sel.cursor = self.textCursor()
            sel.cursor.clearSelection()
            extra.append(sel)
        self.setExtraSelections(extra)
        self.line_number_area.update()