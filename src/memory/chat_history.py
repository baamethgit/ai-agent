"""In-memory chat history using LangChain's built-in store.

Keeps conversation turns in RAM — no persistence between process restarts.
Useful for quick prototyping and classroom demos.

Usage:
    from src.memory.chat_history import get_session_history

    history = get_session_history("alice")
    history.add_user_message("Bonjour!")
    history.add_ai_message("Bonjour, comment puis-je vous aider?")
"""

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

from src.utils.logger import logger

_store: dict[str, ChatMessageHistory] = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Return (or create) the chat history for *session_id*."""
    if session_id not in _store:
        logger.debug("Creating new in-memory history for session '{}'", session_id)
        _store[session_id] = ChatMessageHistory()
    return _store[session_id]


def clear_session_history(session_id: str) -> None:
    """Wipe the history for *session_id* if it exists."""
    if session_id in _store:
        del _store[session_id]
        logger.debug("Cleared history for session '{}'", session_id)


def list_sessions() -> list[str]:
    """Return all active session IDs."""
    return list(_store.keys())


__all__ = ["get_session_history", "clear_session_history", "list_sessions"]
