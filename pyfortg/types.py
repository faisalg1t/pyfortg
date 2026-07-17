"""Telegram API type definitions and Pydantic models."""

from typing import Optional, List, Any, Dict
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict


class User(BaseModel):
    """Telegram User information."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = False
    added_to_attachment_menu: Optional[bool] = False


class Chat(BaseModel):
    """Telegram Chat information."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    type: str  # private, group, supergroup, channel
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    description: Optional[str] = None


class PhotoSize(BaseModel):
    """Telegram Photo Size information."""
    model_config = ConfigDict(from_attributes=True)
    
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: Optional[int] = None


class Document(BaseModel):
    """Telegram Document information."""
    model_config = ConfigDict(from_attributes=True)
    
    file_id: str
    file_unique_id: str
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
    thumbnail: Optional[PhotoSize] = None


class Audio(BaseModel):
    """Telegram Audio information."""
    model_config = ConfigDict(from_attributes=True)
    
    file_id: str
    file_unique_id: str
    duration: int
    performer: Optional[str] = None
    title: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None


class Video(BaseModel):
    """Telegram Video information."""
    model_config = ConfigDict(from_attributes=True)
    
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumbnail: Optional[PhotoSize] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None


class File(BaseModel):
    """Telegram File information."""
    model_config = ConfigDict(from_attributes=True)
    
    file_id: str
    file_unique_id: str
    file_size: Optional[int] = None
    file_path: Optional[str] = None


class InlineButton(BaseModel):
    """Inline button definition."""
    model_config = ConfigDict(from_attributes=True)
    
    text: str
    callback_data: Optional[str] = None
    url: Optional[str] = None
    switch_inline_query: Optional[str] = None
    pay: Optional[bool] = False


class ReplyButton(BaseModel):
    """Reply keyboard button definition."""
    model_config = ConfigDict(from_attributes=True)
    
    text: str
    request_contact: Optional[bool] = False
    request_location: Optional[bool] = False
    request_poll: Optional[Dict[str, Any]] = None


class Message(BaseModel):
    """Telegram Message object."""
    model_config = ConfigDict(from_attributes=True)
    
    message_id: int
    date: int
    chat: Chat
    from_user: Optional[User] = Field(None, alias="from")
    text: Optional[str] = None
    caption: Optional[str] = None
    document: Optional[Document] = None
    photo: Optional[List[PhotoSize]] = None
    audio: Optional[Audio] = None
    video: Optional[Video] = None
    reply_to_message: Optional['Message'] = None
    edit_date: Optional[int] = None
    forward_date: Optional[int] = None
    forward_from: Optional[User] = None
    entities: Optional[List[Dict[str, Any]]] = None


class CallbackQuery(BaseModel):
    """Telegram Callback Query object."""
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    from_user: User = Field(alias="from")
    chat_instance: str
    message: Optional[Message] = None
    inline_message_id: Optional[str] = None
    data: Optional[str] = None
    game_short_name: Optional[str] = None


class Update(BaseModel):
    """Telegram Update object."""
    model_config = ConfigDict(from_attributes=True)
    
    update_id: int
    message: Optional[Message] = None
    edited_message: Optional[Message] = None
    channel_post: Optional[Message] = None
    edited_channel_post: Optional[Message] = None
    callback_query: Optional[CallbackQuery] = None


class APIResponse(BaseModel):
    """Telegram API response wrapper."""
    model_config = ConfigDict(from_attributes=True)
    
    ok: bool
    result: Optional[Any] = None
    error_code: Optional[int] = None
    description: Optional[str] = None


class UpdateType(str, Enum):
    """Telegram Update types."""
    MESSAGE = "message"
    CALLBACK_QUERY = "callback_query"
    CHANNEL_POST = "channel_post"
    EDITED_MESSAGE = "edited_message"
    EDITED_CHANNEL_POST = "edited_channel_post"
    INLINE_QUERY = "inline_query"
    CHOSEN_INLINE_RESULT = "chosen_inline_result"
    SHIPPING_QUERY = "shipping_query"
    PRE_CHECKOUT_QUERY = "pre_checkout_query"
    POLL = "poll"
    POLL_ANSWER = "poll_answer"


# Update forward references
Message.model_rebuild()
