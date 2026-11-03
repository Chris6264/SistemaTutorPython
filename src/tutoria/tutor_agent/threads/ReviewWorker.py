from PySide6.QtCore import QThread, Signal
from tutoria.tutor_agent.agent.TutorAgent import review_code


class ReviewWorker(QThread):
    resultado = Signal(object)
    error = Signal(str)

    def __init__(self, problema: str, codigo: str, salida: str):
        super().__init__()
        self.args = (problema, codigo, salida)

    def run(self):
        try:
            self.resultado.emit(review_code(*self.args))
        except Exception as e:
            self.error.emit(str(e))