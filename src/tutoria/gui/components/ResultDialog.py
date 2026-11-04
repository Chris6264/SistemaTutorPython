from tutoria.gui.components.CustomButton import CustomButton
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QTextEdit, QVBoxLayout

class ResultDialog(QDialog):
        def __init__(self, problem: str, user_output: str, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Resultado de la ejecución")
            self.setModal(True)
            self.resize(800, 700)

            self.problema = self._caja()
            self.problema.setMarkdown(problem)

            self.salida_usuario = self._caja()
            self.salida_usuario.setPlainText(user_output)

            self.salida_esperada = self._caja()
            self.salida_esperada.setPlainText("Calculando...")

            self.veredicto = self._caja()
            self.veredicto.setPlainText("El tutor está revisando tu código...")

            self.close_button = CustomButton("Cerrar")
            self.close_button.clicked.connect(self.accept)

            salidas = QHBoxLayout()
            salidas.addLayout(self._columna("Salida esperada", self.salida_esperada))
            salidas.addLayout(self._columna("Tu salida", self.salida_usuario))

            layout = QVBoxLayout(self)
            layout.addWidget(QLabel("Problema"))
            layout.addWidget(self.problema, 2)
            layout.addLayout(salidas, 2)
            layout.addWidget(QLabel("Veredicto del tutor"))
            layout.addWidget(self.veredicto, 2)
            layout.addWidget(self.close_button)

        def _caja(self) -> QTextEdit:
            box = QTextEdit()
            box.setReadOnly(True)
            return box

        def _columna(self, titulo: str, widget: QTextEdit) -> QVBoxLayout:
            col = QVBoxLayout()
            col.addWidget(QLabel(titulo))
            col.addWidget(widget)
            return col

        def mostrar_revision(self, rev):
            self.salida_esperada.setPlainText(rev.salida_esperada)
            icono = "✅ **¡Correcto!**" if rev.es_correcto else "❌ **Hay algo por corregir**"
            self.veredicto.setMarkdown(f"{icono}\n\n{rev.comentarios}")

        def mostrar_error(self, e: str):
            self.salida_esperada.setPlainText("No disponible")
            self.veredicto.setPlainText(f"No se pudo obtener la revisión: {e}")

        
   
        def mostrar_estadisticas(self, tiempo: str, errores: int, ayudas: int):
            markdown = self.veredicto.toMarkdown()

            markdown += (
                "\n\n---\n\n"
                "### Estadísticas del ejercicio\n\n"
                f"- **Tardaste:** {tiempo}\n"
                f"- **Cometiste:** {errores} errores\n"
                f"- **Ayudas:** {ayudas}\n"
            )

            self.veredicto.setMarkdown(markdown)

                
        def mostrar_evaluacion_difusa(self, puntuacion: float):
                markdown = self.veredicto.toMarkdown()

                markdown += (
                    "\n\n### Evaluación difusa\n\n"
                    f"**Puntuación obtenida:** {puntuacion:.2f}/100\n"
                )

                self.veredicto.setMarkdown(markdown)

        def mostrar_error_difuso(self, error: str):
            markdown = self.veredicto.toMarkdown()

            markdown += (
                "\n\n### Evaluación difusa\n\n"
                "No fue posible calcular el desempeño del alumno."
            )

            self.veredicto.setMarkdown(markdown)
            print(f"Error en FuzzyLevelEvaluator: {error}")

        def agregar_mensaje(self, mensaje: str):
            markdown = self.veredicto.toMarkdown()
            markdown += f"\n\n**{mensaje}**"
            self.veredicto.setMarkdown(markdown)

        def reject(self):
            if self.close_button.isEnabled():
             super().reject()

        def closeEvent(self, event):
            if self.close_button.isEnabled():
                super().closeEvent(event)
            else:
                event.ignore()

                
        def mostrar_resultado_nivel(
            self,
            promedio: float,
            decision: str,
            nivel: str
        ):
            mensajes = {
                "subir": f"¡Felicidades! Ascendiste al nivel {nivel.capitalize()}.",
                "mantener": f"Continuarás practicando en el nivel {nivel.capitalize()}.",
                "bajar": f"Regresarás al nivel {nivel.capitalize()} para reforzar conocimientos."
            }

            markdown = self.veredicto.toMarkdown()

            markdown += (
                "\n\n---\n\n"
                "### Resultado de los dos ejercicios\n\n"
                f"**Promedio final:** {promedio:.2f}/100\n\n"
                f"**Decisión:** {decision.capitalize()}\n\n"
                f"{mensajes[decision]}"
            )

            self.veredicto.setMarkdown(markdown)
