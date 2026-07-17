"""Keyboard builders for Telegram bot interfaces."""

from typing import List, Optional, Dict, Any
from enum import Enum


class ParseMode(str, Enum):
    """Text parsing modes."""
    HTML = "HTML"
    MARKDOWN = "Markdown"
    MARKDOWN_V2 = "MarkdownV2"


class InlineButton:
    """Represents an inline button."""
    
    def __init__(
        self,
        text: str,
        callback_data: Optional[str] = None,
        url: Optional[str] = None,
        switch_inline_query: Optional[str] = None,
        switch_inline_query_current_chat: Optional[str] = None,
        callback_game: bool = False,
        pay: bool = False,
    ):
        self.text = text
        self.callback_data = callback_data
        self.url = url
        self.switch_inline_query = switch_inline_query
        self.switch_inline_query_current_chat = switch_inline_query_current_chat
        self.callback_game = callback_game
        self.pay = pay
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert button to dictionary for API."""
        data = {"text": self.text}
        
        if self.callback_data:
            data["callback_data"] = self.callback_data
        elif self.url:
            data["url"] = self.url
        elif self.switch_inline_query is not None:
            data["switch_inline_query"] = self.switch_inline_query
        elif self.switch_inline_query_current_chat is not None:
            data["switch_inline_query_current_chat"] = self.switch_inline_query_current_chat
        elif self.callback_game:
            data["callback_game"] = self.callback_game
        elif self.pay:
            data["pay"] = self.pay
        
        return data


class KeyboardButton:
    """Represents a reply keyboard button."""
    
    def __init__(
        self,
        text: str,
        request_contact: bool = False,
        request_location: bool = False,
        request_poll: Optional[Dict[str, Any]] = None,
    ):
        self.text = text
        self.request_contact = request_contact
        self.request_location = request_location
        self.request_poll = request_poll
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert button to dictionary for API."""
        data = {"text": self.text}
        
        if self.request_contact:
            data["request_contact"] = True
        elif self.request_location:
            data["request_location"] = True
        elif self.request_poll:
            data["request_poll"] = self.request_poll
        
        return data


class InlineKeyboard:
    """Builder for inline keyboards."""
    
    def __init__(self):
        self.rows: List[List[InlineButton]] = []
    
    def add_button(
        self,
        text: str,
        callback_data: Optional[str] = None,
        url: Optional[str] = None,
    ) -> "InlineKeyboard":
        """Add button to current row."""
        button = InlineButton(text, callback_data=callback_data, url=url)
        if not self.rows:
            self.rows.append([])
        self.rows[-1].append(button)
        return self
    
    def row(self) -> "InlineKeyboard":
        """Start a new row."""
        self.rows.append([])
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API."""
        return {
            "inline_keyboard": [
                [button.to_dict() for button in row]
                for row in self.rows
            ]
        }
    
    def to_json(self) -> str:
        """Convert to JSON string for API."""
        import json
        return json.dumps(self.to_dict())


class ReplyKeyboard:
    """Builder for reply keyboards."""
    
    def __init__(
        self,
        one_time_keyboard: bool = False,
        resize_keyboard: bool = True,
        selective: bool = False,
    ):
        self.rows: List[List[KeyboardButton]] = []
        self.one_time_keyboard = one_time_keyboard
        self.resize_keyboard = resize_keyboard
        self.selective = selective
    
    def add_button(self, text: str) -> "ReplyKeyboard":
        """Add button to current row."""
        button = KeyboardButton(text)
        if not self.rows:
            self.rows.append([])
        self.rows[-1].append(button)
        return self
    
    def add_contact_button(self, text: str = "📱 Share Contact") -> "ReplyKeyboard":
        """Add contact request button."""
        button = KeyboardButton(text, request_contact=True)
        if not self.rows:
            self.rows.append([])
        self.rows[-1].append(button)
        return self
    
    def add_location_button(self, text: str = "📍 Share Location") -> "ReplyKeyboard":
        """Add location request button."""
        button = KeyboardButton(text, request_location=True)
        if not self.rows:
            self.rows.append([])
        self.rows[-1].append(button)
        return self
    
    def row(self) -> "ReplyKeyboard":
        """Start a new row."""
        self.rows.append([])
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API."""
        return {
            "keyboard": [
                [button.to_dict() for button in row]
                for row in self.rows
            ],
            "one_time_keyboard": self.one_time_keyboard,
            "resize_keyboard": self.resize_keyboard,
            "selective": self.selective,
        }
    
    def to_json(self) -> str:
        """Convert to JSON string for API."""
        import json
        return json.dumps(self.to_dict())


class RemoveKeyboard:
    """Remove reply keyboard."""
    
    def __init__(self, selective: bool = False):
        self.selective = selective
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "remove_keyboard": True,
            "selective": self.selective,
        }
    
    def to_json(self) -> str:
        """Convert to JSON string for API."""
        import json
        return json.dumps(self.to_dict())


class ForceReply:
    """Force reply keyboard."""
    
    def __init__(self, selective: bool = False, input_field_placeholder: Optional[str] = None):
        self.selective = selective
        self.input_field_placeholder = input_field_placeholder
    
    def to_dict(self) -> Dict[str, Any]:
        data = {
            "force_reply": True,
            "selective": self.selective,
        }
        if self.input_field_placeholder:
            data["input_field_placeholder"] = self.input_field_placeholder
        return data
    
    def to_json(self) -> str:
        """Convert to JSON string for API."""
        import json
        return json.dumps(self.to_dict())
