from PySide6.QtCore import QThread, Signal
from tutoria.tutor_agent.agent.TutorAgent import preguntar_stream


class StreamWorker(QThread):
    token = Signal(str)
    terminado = Signal()
    error = Signal(str)

    def __init__(self, texto: str):
        super().__init__()
        self.texto = texto

    def run(self):
        try:
            for t in preguntar_stream(self.texto):
                self.token.emit(t)
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.terminado.emit()