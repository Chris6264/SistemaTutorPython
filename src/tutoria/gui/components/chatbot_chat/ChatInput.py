from PySide6.QtCore import QEvent, Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

MAX_LINES = 5


class _InputEdit(QPlainTextEdit):
    submitted = Signal()

    def keyPressEvent(self, event):
        is_enter = event.key() in (Qt.Key_Return, Qt.Key_Enter)
        if is_enter and not (event.modifiers() & Qt.ShiftModifier):
            self.submitted.emit()
            return
        super().keyPressEvent(event)


class ChatInput(QWidget):
    submitted = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.edit = _InputEdit()
        self.edit.setObjectName("ChatInputText")
        self.edit.setPlaceholderText("Escribe tu pregunta...")
        self.edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.edit.setTabChangesFocus(True)

        self.send_button = QPushButton("↑")
        self.send_button.setObjectName("SendButton")
        self.send_button.setFixedSize(34, 34)
        self.send_button.setCursor(Qt.PointingHandCursor)
        self.send_button.setEnabled(False)

        box = QFrame()
        box.setObjectName("ChatInputBox")
        box_layout = QHBoxLayout(box)
        box_layout.setContentsMargins(14, 6, 6, 6)
        box_layout.setSpacing(8)
        box_layout.addWidget(self.edit, 1)
        box_layout.addWidget(self.send_button, alignment=Qt.AlignBottom)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.addWidget(box)

        self.edit.textChanged.connect(self._update_send_state)
        self.edit.submitted.connect(self._send)
        self.send_button.clicked.connect(self._send)
        self.edit.document().documentLayout().documentSizeChanged.connect(
            self._fit_height
        )
        self.edit.ensurePolished()
        self._fit_height()

    def _fit_height(self, *_):
        doc = self.edit.document()
        total_lines = int(doc.size().height())
        lines = max(1, min(total_lines, MAX_LINES))
        extra = int(doc.documentMargin() * 2) + 2
        self.edit.setFixedHeight(lines * self.edit.fontMetrics().lineSpacing() + extra)
        self.edit.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded if total_lines > MAX_LINES else Qt.ScrollBarAlwaysOff
        )

    def showEvent(self, event):
        super().showEvent(event)
        self._fit_height()

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() in (QEvent.FontChange, QEvent.StyleChange):
            self._fit_height()

    def _update_send_state(self):
        has_text = bool(self.edit.toPlainText().strip())
        self.send_button.setEnabled(has_text and not self.edit.isReadOnly())

    def _send(self):
        text = self.edit.toPlainText().strip()
        if not text or self.edit.isReadOnly():
            return
        self.edit.clear()
        self.submitted.emit(text)

    def set_busy(self, busy: bool):
        self.edit.setReadOnly(busy)
        self._update_send_state()

    def focus_input(self):
        self.edit.setFocus()