
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget
from tutoria.gui.components.CustomTextEdit import CustomTextEdit
from tutoria.gui.components.code_editor.CodeEditor import CodeEditor
from tutoria.gui.components.CustomButton import CustomButton
from tutoria.gui.components.CustomCounter import CustomCounter
from tutoria.gui.components.ChatBotChat import ChatBotChat
from tutoria.gui.components.chatbot_chat.StreamWorker import StreamWorker
from tutoria.gui.components.DigitalChronometer import DigitalChronometer
from tutoria.tutor_agent.agent.TutorAgent import preguntar
from tutoria.tutor_agent.prompts.TutorPrompt import MENSAJE_INICIO
from contextlib import redirect_stdout

import io

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema Tutor De Python - Nivel 1")
        self.resize(1024, 768)
        self.setMinimumSize(800, 600)

        self.worker = None
        self.respuesta_actual = ""
        self.bot_message = None

        principal_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        information_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        self.code_editor = CodeEditor()
        help_button = CustomButton("Help")
        compile_button = CustomButton("Compilar")
        self.run_button = CustomButton("Run")
        self.problem_header = CustomTextEdit("Descripcion del problema")
        self.errors_counter = CustomCounter("Errores")
        self.chat_bot = ChatBotChat()
        self.console_text = CustomTextEdit("Salida del programa")
        digital_chronometer = DigitalChronometer()

        compile_button.clicked.connect(self.compile_code)
        help_button.clicked.connect(self.toggle_show_chatbot)
        self.run_button.clicked.connect(self.execute_code)
        self.code_editor.textChanged.connect(self.text_changed)

        self.problem_header.setMarkdown(preguntar(MENSAJE_INICIO))
        digital_chronometer.start_chronometer()
        self.run_button.setEnabled(False)
        self.chat_bot.setVisible(False)
        self.chat_bot.add_bot_message("¡Hola! Soy tu tutor. Pídeme ayuda cuando la necesites.")
        self.chat_bot.message_sent.connect(self.on_user_message)

        left_layout.addWidget(self.problem_header)
        left_layout.addWidget(self.code_editor)

        button_layout.addWidget(compile_button)
        button_layout.addWidget(self.run_button)

        information_layout.addWidget(help_button)
        information_layout.addWidget(self.errors_counter)
        information_layout.addWidget(digital_chronometer)

        right_layout.addWidget(self.console_text, 1)
        right_layout.addLayout(button_layout)
        right_layout.addWidget(self.chat_bot, 1)
        right_layout.addLayout(information_layout)

        principal_layout.addLayout(left_layout,2)
        principal_layout.addLayout(right_layout,2)

        container = QWidget()
        container.setLayout(principal_layout)
        self.setCentralWidget(container)

    def toggle_show_chatbot(self):
        self.chat_bot.setVisible(not self.chat_bot.isVisible())

    def text_changed(self):
        self.run_button.setEnabled(False)

    def review_syntax(self, codigo) -> str | None:
        try:
            compile(codigo, "<alumno>", "exec")
            return None
        except SyntaxError as e:
            return f"Línea {e.lineno}: {e.msg}"

    def compile_code(self):
        self.code = self.code_editor.toPlainText()

        if not self.code.strip():
            self.console_text.setPlainText("Escribe algo de código primero.")
            return
        
        error = self.review_syntax(self.code)

        if error:
            self.console_text.setPlainText(f"Error de sintaxis\n{error}")
            self.run_button.setEnabled(False)
            new_counter = self.errors_counter.get_counter() + 1
            self.errors_counter.set_counter(new_counter)
        else:
            self.console_text.setPlainText("Sin errores de sintaxis.")
            self.run_button.setEnabled(True)

    def execute_code(self):
        string_io = io.StringIO()
        try:
            with redirect_stdout(string_io):
                exec(self.code)

            output = string_io.getvalue()
            self.console_text.setText(output)
            return True
        except Exception as e:
           self.console_text.setText(f"Error durante la ejecución del código: {e}")
           return False

    def on_user_message(self, text: str):
        if self.worker and self.worker.isRunning():
            return
        self.respuesta_actual = ""
        self.bot_message = self.chat_bot.add_bot_message("...")
        self.chat_bot.set_busy(True)

        self.worker = StreamWorker(text)
        self.worker.token.connect(self.on_token)
        self.worker.error.connect(self.on_stream_error)
        self.worker.finished.connect(lambda: self.chat_bot.set_busy(False))
        self.worker.start()

    def on_token(self, t: str):
        self.respuesta_actual += t
        self.bot_message.set_text(self.respuesta_actual)
        self.chat_bot.scroll_to_bottom()

    def on_stream_error(self, e: str):
        self.bot_message.set_text(f"Error: {e}")