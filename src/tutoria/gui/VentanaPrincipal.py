import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from tutoria.gui.components.MainWindow import MainWindow

app = QApplication(sys.argv)
app.setStyleSheet(Path("src/tutoria/gui/styles/styles.qss").read_text(encoding="utf-8"))

window = MainWindow()
window.show()

sys.exit(app.exec())