from pathlib import Path

from tutoria.gui.components.chatbot_chat.ChatMessage import ChatMessage

BOT_ICON = Path(__file__).resolve().parents[2] / "assets" / "icons" / "icon.png"


class BotMessage(ChatMessage):
    def __init__(self, text: str = "", parent=None):
        super().__init__(
            text=text,
            icon_path=BOT_ICON,
            side="left",
            bubble_bg="#f1f5f9",
            bubble_border="#cbd5e1",
            avatar_bg="#000000",
            text_object_name="BotBubbleText",
            icon_ratio=0.75,
            markdown=True,
            parent=parent,
        )