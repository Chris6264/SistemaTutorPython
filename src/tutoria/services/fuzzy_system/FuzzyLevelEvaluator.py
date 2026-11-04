
from itertools import product

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class FuzzyLevelEvaluator:
    """Evalúa el desempeño del alumno mediante lógica difusa Mamdani."""

    def __init__(self):
        self.tiempo = ctrl.Antecedent(
            np.arange(0, 30.1, 0.1), "tiempo"
        )
        self.errores = ctrl.Antecedent(
            np.arange(0, 10.1, 0.1), "errores"
        )
        self.ayudas = ctrl.Antecedent(
            np.arange(0, 10.1, 0.1), "ayudas"
        )
        self.desempeno = ctrl.Consequent(
            np.arange(0, 101, 1), "desempeno"
        )

        self.tiempo["rapido"] = fuzz.trimf(
            self.tiempo.universe, [0, 0, 12]
        )
        self.tiempo["normal"] = fuzz.trimf(
            self.tiempo.universe, [7, 15, 23]
        )
        self.tiempo["lento"] = fuzz.trimf(
            self.tiempo.universe, [18, 30, 30]
        )

        self.errores["pocos"] = fuzz.trimf(
            self.errores.universe, [0, 0, 3]
        )
        self.errores["moderados"] = fuzz.trimf(
            self.errores.universe, [1, 4, 7]
        )
        self.errores["muchos"] = fuzz.trimf(
            self.errores.universe, [5, 10, 10]
        )

        self.ayudas["pocas"] = fuzz.trimf(
            self.ayudas.universe, [0, 0, 3]
        )
        self.ayudas["moderadas"] = fuzz.trimf(
            self.ayudas.universe, [1, 4, 7]
        )
        self.ayudas["muchas"] = fuzz.trimf(
            self.ayudas.universe, [5, 10, 10]
        )

        self.desempeno["bajo"] = fuzz.trimf(
            self.desempeno.universe, [0, 0, 40]
        )
        self.desempeno["medio"] = fuzz.trimf(
            self.desempeno.universe, [30, 50, 70]
        )
        self.desempeno["alto"] = fuzz.trimf(
            self.desempeno.universe, [60, 100, 100]
        )

        reglas = self._crear_reglas()
        self.sistema = ctrl.ControlSystem(reglas)

    def _crear_reglas(self):
        categorias = [
            ("rapido", "normal", "lento"),
            ("pocos", "moderados", "muchos"),
            ("pocas", "moderadas", "muchas")
        ]

        puntuaciones = {
            "rapido": 2, "normal": 1, "lento": 0,
            "pocos": 2, "moderados": 1, "muchos": 0,
            "pocas": 2, "moderadas": 1, "muchas": 0
        }

        reglas = []

        for tiempo, errores, ayudas in product(*categorias):
            total = (
                puntuaciones[tiempo]
                + puntuaciones[errores]
                + puntuaciones[ayudas]
            )

            if total >= 5:
                salida = "alto"
            elif total >= 3:
                salida = "medio"
            else:
                salida = "bajo"

            regla = ctrl.Rule(
                self.tiempo[tiempo]
                & self.errores[errores]
                & self.ayudas[ayudas],
                self.desempeno[salida]
            )
            reglas.append(regla)

        return reglas

    def evaluar(
        self, tiempo_minutos: float, errores: int, ayudas: int
    ) -> dict:
        if tiempo_minutos < 0 or errores < 0 or ayudas < 0:
            raise ValueError("Las entradas no pueden ser negativas.")

        simulacion = ctrl.ControlSystemSimulation(self.sistema)

        simulacion.input["tiempo"] = min(tiempo_minutos, 30)
        simulacion.input["errores"] = min(errores, 10)
        simulacion.input["ayudas"] = min(ayudas, 10)

        simulacion.compute()

        puntuacion = float(simulacion.output["desempeno"])

        if puntuacion >= 65:
            decision = "subir"
        elif puntuacion >= 35:
            decision = "mantener"
        else:
            decision = "bajar"

        return {
            "puntuacion": round(puntuacion, 2),
            "decision": decision
        }