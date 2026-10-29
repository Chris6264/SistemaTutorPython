from pathlib import Path

from tutoria.gui.components.chatbot_chat.ChatMessage import ChatMessage

USER_ICON = Path(__file__).resolve().parents[2] / "assets" / "icons" / "user_icon.png"


class UserMessage(ChatMessage):
    def __init__(self, text: str = "", parent=None):
        super().__init__(
            text=text,
            icon_path=USER_ICON,
            side="right",
            bubble_bg="#dbeafe",
            bubble_border="#bfdbfe",
            avatar_bg="#FFCACA",
            text_object_name="UserBubbleText",
            icon_ratio=0.55,
            markdown=False,
            parent=parent,
        )