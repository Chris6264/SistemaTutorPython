from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessageChunk
from langgraph.checkpoint.memory import InMemorySaver
from tutoria.tutor_agent.prompts.TutorPrompt import build_system_prompt
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(model="openai/gpt-oss-120b")

agent = create_agent(
    model = model,
    system_prompt=build_system_prompt("basico","basico"),
    checkpointer=InMemorySaver(),
    tools=[]
    )

def preguntar(texto: str, thread_id: str = "alumno") -> str:
    resultado = agent.invoke(
        {"messages": [{"role": "user", "content": texto}]},
        config={"configurable": {"thread_id": thread_id}},
    )
    return resultado["messages"][-1].content

def preguntar_stream(texto: str, thread_id: str = "alumno"):
    for chunk, metadata in agent.stream(
        {"messages": [{"role": "user", "content": texto}]},
        config={"configurable": {"thread_id": thread_id}},
        stream_mode="messages",
    ):

        if isinstance(chunk, AIMessageChunk) and chunk.content:
            if isinstance(chunk.content, str):
                yield chunk.content
 