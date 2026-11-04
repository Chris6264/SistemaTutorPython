class LevelProgressionManager:
    """Administra la progresión del alumno mediante puntuaciones difusas."""

    NIVELES = ("basico", "intermedio", "avanzado")

    def __init__(self):
        self.nivel_actual = "basico"
        self.puntuaciones = []
        self.ejercicios_por_etapa = 2

    def registrar_resultado(self, puntuacion: float) -> dict:
        if not 0 <= puntuacion <= 100:
            raise ValueError("La puntuación debe estar entre 0 y 100.")

        self.puntuaciones.append(puntuacion)

        if len(self.puntuaciones) < self.ejercicios_por_etapa:
            return {
                "evaluacion_completa": False,
                "nivel_actual": self.nivel_actual,
                "ejercicios_completados": len(self.puntuaciones),
                "decision": None,
                "promedio": None,
                "cambio_nivel": False
            }

        promedio = sum(self.puntuaciones) / len(self.puntuaciones)
        nivel_anterior = self.nivel_actual
        decision = self._determinar_decision(promedio)

        indice = self.NIVELES.index(self.nivel_actual)

        if decision == "subir":
            self.nivel_actual = self.NIVELES[indice + 1]
        elif decision == "bajar":
            self.nivel_actual = self.NIVELES[indice - 1]

        self.puntuaciones.clear()

        return {
            "evaluacion_completa": True,
            "nivel_anterior": nivel_anterior,
            "nivel_actual": self.nivel_actual,
            "ejercicios_completados": 2,
            "decision": decision,
            "promedio": round(promedio, 2),
            "cambio_nivel": nivel_anterior != self.nivel_actual
        }

    def _determinar_decision(self, promedio: float) -> str:
        if self.nivel_actual == "basico":
            return "subir" if promedio >= 65 else "mantener"

        if self.nivel_actual == "intermedio":
            if promedio < 50:
                return "bajar"
            if promedio >= 75:
                return "subir"
            return "mantener"

        if self.nivel_actual == "avanzado":
            return "bajar" if promedio < 70 else "mantener"

        raise ValueError("Nivel no reconocido.")