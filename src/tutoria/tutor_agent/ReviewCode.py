from pydantic import BaseModel, Field

class ReviewCode(BaseModel):
    salida_esperada: str = Field(description="Salida exacta que debería producir un programa correcto")
    es_correcto: bool = Field(description="True si la salida del alumno coincide con la esperada")
    comentarios: str = Field(description="Retroalimentación breve en Markdown, sin dar la solución completa")
