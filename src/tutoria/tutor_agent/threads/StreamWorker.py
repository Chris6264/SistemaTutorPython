from PySide6.QtCore import QThread, Signal
from tutoria.tutor_agent.agent.TutorAgent import preguntar_stream


class StreamWorker(QThread):
    token = Signal(str)
    terminado = Signal()
    error = Signal(str)

    def __init__(self, texto: str, thread_id: str = "alumno"):
        super().__init__()
        self.texto = texto
        self.thread_id = thread_id

    def run(self):
        try:
            for token in preguntar_stream(
                self.texto,
                thread_id=self.thread_id
            ):
                self.token.emit(token)
        except Exception as error:
            self.error.emit(str(error))