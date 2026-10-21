
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

        help_button = CustomButton("Help")
        compile_button = CustomButton("Compilar")
        run_button = CustomButton("Run")

        problem_header = CustomTextEdit("Descripcion del problema")
        code_editor = CodeEditor("Editor De Codigo")

        errors_counter = CustomCounter("Errores")
        time_counter = CustomCounter("Tiempo")

        self.chat_bot = ChatBotChat()
        console_text = CustomTextEdit("Salida del programa")


        left_layout.addWidget(problem_header)
        left_layout.addWidget(code_editor)

        button_layout.addWidget(compile_button)
        button_layout.addWidget(run_button)

        help_button.clicked.connect(self.alternar_mostrar_chatbot)

        information_layout.addWidget(help_button)
        information_layout.addWidget(errors_counter)
        information_layout.addWidget(time_counter)

        right_layout.addWidget(console_text)
        right_layout.addLayout(button_layout)
        right_layout.addWidget(self.chat_bot)
        right_layout.addLayout(information_layout)

        principal_layout.addLayout(left_layout,2)
        principal_layout.addLayout(right_layout,2)

        

        container = QWidget()
        container.setLayout(principal_layout)
        self.setCentralWidget(container)

    def alternar_mostrar_chatbot(self):
        self.chat_bot.setVisible(not self.chat_bot.isVisible())




