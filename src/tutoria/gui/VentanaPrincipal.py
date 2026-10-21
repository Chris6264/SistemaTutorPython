import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from tutoria.gui.components.MainWindow import MainWindow

app = QApplication(sys.argv)

ruta = Path(__file__).resolve().parent / "styles/theme.qss"
app.setStyleSheet(ruta.read_text(encoding="utf-8"))

window = MainWindow()
window.show()

sys.exit(app.exec())