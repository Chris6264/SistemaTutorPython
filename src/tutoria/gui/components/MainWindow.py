
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QInputDialog
from tutoria.gui.components.CustomTextEdit import CustomTextEdit
from tutoria.gui.components.code_editor.CodeEditor import CodeEditor
from tutoria.gui.components.CustomButton import CustomButton
from tutoria.gui.components.CustomCounter import CustomCounter
from tutoria.gui.components.ChatBotChat import ChatBotChat
from tutoria.gui.components.DigitalChronometer import DigitalChronometer
from tutoria.gui.components.ResultDialog import ResultDialog
from tutoria.tutor_agent.agent.TutorAgent import preguntar
from tutoria.tutor_agent.prompts.TutorPrompt import MENSAJE_INICIO
from tutoria.tutor_agent.threads.StreamWorker import StreamWorker
from tutoria.tutor_agent.threads.ReviewWorker import ReviewWorker
from tutoria.services.fuzzy_system.FuzzyLevelEvaluator import FuzzyLevelEvaluator
from tutoria.services.fuzzy_system.LevelProgressionManager import LevelProgressionManager
from tutoria.tutor_agent.agent.TutorAgent import configurar_nivel
from contextlib import redirect_stdout
from uuid import uuid4

import io

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TutorIA - Nivel Basico")
        self.resize(1024, 768)
        self.setMinimumSize(800, 600)
        
        self.worker = None
        self.respuesta_actual = ""
        self.bot_message = None
        self.review_worker = None
        self.help_counter = 0
        self.exercise_completed = False
        self.nivel_actual = "basico"

        principal_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        information_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        self.level_manager = LevelProgressionManager()
        self.fuzzy_evaluator = FuzzyLevelEvaluator()
        self.nivel_actual = self.level_manager.nivel_actual
        self.nivel_actual_agente = "basico"
        self.thread_id = uuid4().hex
        self.siguiente_problema_pendiente = False
        self.code_editor = CodeEditor()
        help_button = CustomButton("Help")
        compile_button = CustomButton("Compilar")
        self.run_button = CustomButton("Run")
        self.problem_header = CustomTextEdit("Descripcion del problema")
        self.errors_counter = CustomCounter("Errores")
        self.chat_bot = ChatBotChat()
        self.console_text = CustomTextEdit("Salida del programa")
        self.digital_chronometer = DigitalChronometer()

        compile_button.clicked.connect(self.compile_code)
        help_button.clicked.connect(self.toggle_show_chatbot)
        self.run_button.clicked.connect(self.execute_code)
        self.code_editor.textChanged.connect(self.text_changed)

        self.problem_header.setMarkdown(preguntar(MENSAJE_INICIO,thread_id=self.thread_id))
        self.digital_chronometer.start_chronometer()
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
        information_layout.addWidget(self.digital_chronometer)

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
        if self.exercise_completed:
            self.console_text.setPlainText("Este ejercicio ya fue completado.")
            return

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
        if self.exercise_completed:
            return False

        if self.review_worker is not None and self.review_worker.isRunning():
            return False

        self.code = self.code_editor.toPlainText()

        if not self.code.strip():
            self.console_text.setPlainText("Escribe algo de código primero.")
            return False

        error = self.review_syntax(self.code)

        if error:
            self.console_text.setPlainText(f"Error de sintaxis\n{error}")
            self.errors_counter.set_counter(
                self.errors_counter.get_counter() + 1
            )
            return False

        string_io = io.StringIO()

        try:
            with redirect_stdout(string_io):
                exec(
                    self.code,
                    {
                        "__name__": "__main__",
                        "input": self.solicitar_entrada
                    }
                )

            output = string_io.getvalue()
            self.console_text.setPlainText(output)
            self.open_review(output)
            return True

        except EOFError:
            self.console_text.setPlainText(
                "La entrada de datos fue cancelada."
            )
            return False

        except Exception as e:
            self.console_text.setPlainText(
                f"Error durante la ejecución del código: {e}"
            )
            self.errors_counter.set_counter(
                self.errors_counter.get_counter() + 1
            )
            return False
        
    def on_user_message(self, text: str):
        if self.worker and self.worker.isRunning():
            return

        self.help_counter += 1
        self.respuesta_actual = ""
        self.bot_message = self.chat_bot.add_bot_message("...")
        self.chat_bot.set_busy(True)
        self.worker = StreamWorker(text, self.thread_id)    
        self.worker.token.connect(self.on_token)
        self.worker.error.connect(self.on_stream_error)
        self.worker.finished.connect(
            lambda: self.chat_bot.set_busy(False)
        )
        self.worker.start()

    def on_token(self, t: str):
        self.respuesta_actual += t
        self.bot_message.set_text(self.respuesta_actual)
        self.chat_bot.scroll_to_bottom()

    def on_stream_error(self, e: str):
        self.bot_message.set_text(f"Error: {e}")

    

    def open_review(self, output: str):
        dialog = ResultDialog(
            self.problem_header.toMarkdown(),
            output,
            parent=self
        )

        self.result_dialog = dialog
        self.run_button.setEnabled(False)

        self.review_worker = ReviewWorker(
            self.problem_header.toPlainText(),
            self.code,
            output
        )

        dialog.close_button.setEnabled(False)

        self.review_worker.resultado.connect(dialog.mostrar_revision)
        self.review_worker.resultado.connect(self.on_review_completed)
        self.review_worker.error.connect(dialog.mostrar_error)
        self.review_worker.finished.connect(self.on_review_finished)
        self.review_worker.finished.connect(
            lambda: dialog.close_button.setEnabled(True)
        )

        self.review_worker.start()
        dialog.exec()

        if self.siguiente_problema_pendiente:
            self.siguiente_problema()


    def on_review_completed(self, review):
        if self.exercise_completed:
            return

        if not review.es_correcto:
            self.errors_counter.set_counter(
                self.errors_counter.get_counter() + 1
            )
            return

        self.exercise_completed = True
        self.digital_chronometer.pause_chronometer()
        self.run_button.setEnabled(False)

        tiempo = self.digital_chronometer.get_elapsed_time()
        errores = self.errors_counter.get_counter()
        ayudas = self.help_counter

        minutos, segundos = map(int, tiempo.split(":"))
        tiempo_minutos = minutos + segundos / 60

        self.result_dialog.mostrar_estadisticas(
            tiempo, errores, ayudas
        )

        try:
            resultado = self.fuzzy_evaluator.evaluar(
                tiempo_minutos=tiempo_minutos,
                errores=errores,
                ayudas=ayudas
            )

            progresion = self.level_manager.registrar_resultado(
                resultado["puntuacion"]
            )

            self.result_dialog.mostrar_evaluacion_difusa(
                resultado["puntuacion"]
            )

            if not progresion["evaluacion_completa"]:
                self.result_dialog.agregar_mensaje(
                    "¡Primer ejercicio completado! "
                    "Continúa con el segundo para determinar tu nivel."
                )
            else:
                self.result_dialog.mostrar_resultado_nivel(
                    progresion["promedio"],
                    progresion["decision"],
                    progresion["nivel_actual"]
                )

            self.nivel_actual = progresion["nivel_actual"]

        except Exception as error:
            self.result_dialog.mostrar_error_difuso(str(error))

        self.siguiente_problema_pendiente = True


    def on_review_finished(self):
        if not self.exercise_completed:
            self.run_button.setEnabled(True)

    
    def siguiente_problema(self):
        nivel = self.level_manager.nivel_actual
        cambio_nivel = nivel != self.nivel_actual_agente

        if cambio_nivel:
            configurar_nivel(nivel)
            self.nivel_actual_agente = nivel

        self.thread_id = uuid4().hex

        self.chat_bot.clear_chat()
        self.bot_message = None
        self.respuesta_actual = ""
        self.help_counter = 0

        mensaje = (
            "[INICIO_DE_SESION]" if cambio_nivel
            else "[NUEVO_PROBLEMA]"
        )

        try:
            problema = preguntar(
                mensaje,
                thread_id=self.thread_id
            )
        except Exception as error:
            self.console_text.setPlainText(
                f"No se pudo generar el siguiente problema: {error}"
            )
            return

        self.problem_header.setMarkdown(problema)
        self.code_editor.clear()
        self.console_text.clear()

        self.errors_counter.set_counter(0)
        self.help_counter = 0

        self.digital_chronometer.restart_chronometer()
        self.digital_chronometer.start_chronometer()

        self.exercise_completed = False
        self.siguiente_problema_pendiente = False

        self.run_button.setEnabled(False)

        self.setWindowTitle(
            f"TutorIA - Nivel {nivel.capitalize()}"
        )


    def solicitar_entrada(self, mensaje: str = "") -> str:
        texto, aceptado = QInputDialog.getText(
            self,
            "Entrada de datos",
            mensaje or "Introduce un valor:"
        )

        if not aceptado:
            raise EOFError("El alumno canceló la entrada.")

        return texto
