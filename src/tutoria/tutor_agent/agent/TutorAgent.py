from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessageChunk
from langgraph.checkpoint.memory import InMemorySaver
from tutoria.tutor_agent.prompts.TutorPrompt import build_system_prompt
from tutoria.tutor_agent.ReviewCode import ReviewCode
from dotenv import load_dotenv

load_dotenv()

NIVELES_DISPONIBLES = ("basico", "intermedio", "avanzado")

model = ChatGroq(model="openai/gpt-oss-120b")

checkpointer = InMemorySaver()


def crear_agente(nivel: str):
    """Crea un agente configurado para el nivel indicado."""

    if nivel not in NIVELES_DISPONIBLES:
        raise ValueError(f"Nivel no válido: {nivel}")

    return create_agent(
        model=model,
        system_prompt=build_system_prompt(
            nivel_actual=nivel,
            niveles_disponibles=", ".join(NIVELES_DISPONIBLES)
        ),
        checkpointer=checkpointer
    )


agent = crear_agente("basico")


def configurar_nivel(nivel: str):
    """Actualiza el agente para trabajar con otro nivel."""

    global agent
    agent = crear_agente(nivel)


def preguntar(texto: str, thread_id: str = "alumno") -> str:
    """Envía un mensaje al agente y devuelve su respuesta."""

    resultado = agent.invoke(
        {"messages": [{"role": "user", "content": texto}]},
        config={
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    return resultado["messages"][-1].content


def preguntar_stream(texto: str, thread_id: str = "alumno"):
    """Genera la respuesta del agente mediante streaming."""

    for chunk, metadata in agent.stream(
        {"messages": [{"role": "user", "content": texto}]},
        config={
            "configurable": {
                "thread_id": thread_id
            }
        },
        stream_mode="messages"
    ):

        if isinstance(chunk, AIMessageChunk) and chunk.content:
            if isinstance(chunk.content, str):
                yield chunk.content


def review_code(problema: str, codigo: str, salida: str) -> ReviewCode:
    """Evalúa el código del alumno mediante una salida estructurada."""

    prompt = f"""Eres un tutor profesional de Python.
    Revisa la solución de un alumno.

    PROBLEMA:
    {problema}

    CÓDIGO DEL ALUMNO:
    ```python
    {codigo}
    ```

    SALIDA OBTENIDA:
    {salida}

    INSTRUCCIONES:
    - Determina la salida esperada según el problema.
    - Comprueba si el código resuelve correctamente el ejercicio.
    - Evalúa la lógica, no solamente la salida mostrada.
    - Indica si el alumno acertó.
    - Proporciona comentarios breves.
    - Si hay errores, ofrece pistas sin entregar el código completo.
    - No propongas otro ejercicio durante la revisión.
    - No inventes resultados de ejecución.

    Devuelve la evaluación siguiendo el esquema ReviewCode.
    """

    return model.with_structured_output(ReviewCode).invoke(prompt)