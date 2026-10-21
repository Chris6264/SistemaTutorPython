
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget
from tutoria.gui.components.CustomTextEdit import CustomTextEdit
from tutoria.gui.components.CodeEditor import CodeEditor
from tutoria.gui.components.CustomButton import CustomButton
from tutoria.gui.components.CustomCounter import CustomCounter
from tutoria.gui.components.ChatBotChat import ChatBotChat

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema Tutor De Python - Nivel 1")
        self.resize(1024, 768)
        self.setMinimumSize(800, 600)

        principal_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        information_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        left_layout.addWidget(CustomTextEdit())
        left_layout.addWidget(CodeEditor())

        button_layout.addWidget(CustomButton("Compilar"))
        button_layout.addWidget(CustomButton("Run"))

        information_layout.addWidget(CustomButton("Help"))
        information_layout.addWidget(CustomCounter("Errores"))
        information_layout.addWidget(CustomCounter("Tiempo"))

        right_layout.addWidget(CustomTextEdit())
        right_layout.addLayout(button_layout)
        right_layout.addWidget(ChatBotChat())
        right_layout.addLayout(information_layout)

        principal_layout.addLayout(left_layout,2)
        principal_layout.addLayout(right_layout,2)

        container = QWidget()
        container.setLayout(principal_layout)
        self.setCentralWidget(container)



