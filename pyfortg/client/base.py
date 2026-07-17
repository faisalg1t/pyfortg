"""Base Telegram client implementation."""

import asyncio
import json
import logging
from typing import Optional, Dict, Any, List, BinaryIO
from urllib.parse import urljoin

import aiohttp

from ..types import Update, APIResponse, Message, CallbackQuery, User, File
from ..exceptions import APIException, ValidationException, TimeoutException, ConnectionException

logger = logging.getLogger(__name__)


class TelegramClient:
    """Base Telegram Bot API client."""
    
    BASE_URL = "https://api.telegram.org"
    
    def __init__(
        self,
        token: str,
        timeout: int = 30,
        session: Optional[aiohttp.ClientSession] = None,
    ):
        """
        Initialize Telegram client.
        
        Args:
            token: Telegram bot token
            timeout: Request timeout in seconds
            session: Optional aiohttp ClientSession
        """
        self.token = token
        self.timeout = timeout
        self.session = session
        self._own_session = session is None
        self.base_url = f"{self.BASE_URL}/bot{token}"
    
    async def __aenter__(self):
        """Async context manager entry."""
        if self._own_session:
            self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
    
    async def close(self):
        """Close the client session."""
        if self._own_session and self.session:
            await self.session.close()
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, BinaryIO]] = None,
    ) -> Dict[str, Any]:
        """
        Make a request to Telegram API.
        
        Args:
            method: HTTP method (GET, POST)
            endpoint: API endpoint
            data: Request data
            files: Files to upload
        
        Returns:
            API response data
        
        Raises:
            APIException: If API returns error
            TimeoutException: If request times out
            ConnectionException: If connection fails
        """
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        url = urljoin(self.base_url, endpoint)
        
        try:
            async with asyncio.timeout(self.timeout):
                if files:
                    async with self.session.post(url, data=data, files=files) as resp:
                        return await self._handle_response(resp)
                else:
                    async with self.session.request(
                        method,
                        url,
                        json=data if method == "POST" else None,
                        params=data if method == "GET" else None,
                    ) as resp:
                        return await self._handle_response(resp)
        except asyncio.TimeoutError:
            raise TimeoutException(f"Request to {endpoint} timed out after {self.timeout}s")
        except aiohttp.ClientError as e:
            raise ConnectionException(f"Connection error: {str(e)}")
    
    async def _handle_response(self, resp: aiohttp.ClientResponse) -> Dict[str, Any]:
        """Handle API response."""
        try:
            data = await resp.json()
        except json.JSONDecodeError:
            text = await resp.text()
            raise APIException(
                resp.status,
                f"Invalid JSON response: {text[:100]}",
            )
        
        if not data.get("ok", False):
            raise APIException(
                data.get("error_code", resp.status),
                data.get("description", "Unknown error"),
                data,
            )
        
        return data.get("result", {})
    
    # Message sending methods
    
    async def send_message(
        self,
        chat_id: int,
        text: str,
        parse_mode: Optional[str] = None,
        reply_markup: Optional[Dict[str, Any]] = None,
        disable_web_page_preview: bool = False,
        disable_notification: bool = False,
        reply_to_message_id: Optional[int] = None,
    ) -> Message:
        """Send text message."""
        data = {
            "chat_id": chat_id,
            "text": text,
        }
        if parse_mode:
            data["parse_mode"] = parse_mode
        if reply_markup:
            data["reply_markup"] = reply_markup
        if disable_web_page_preview:
            data["disable_web_page_preview"] = True
        if disable_notification:
            data["disable_notification"] = True
        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id
        
        result = await self._request("POST", "sendMessage", data)
        return Message(**result)
    
    async def edit_message_text(
        self,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        text: str = "",
        parse_mode: Optional[str] = None,
        reply_markup: Optional[Dict[str, Any]] = None,
    ) -> Message:
        """Edit text message."""
        data = {"text": text}
        
        if chat_id is not None and message_id is not None:
            data["chat_id"] = chat_id
            data["message_id"] = message_id
        elif inline_message_id:
            data["inline_message_id"] = inline_message_id
        else:
            raise ValidationException("Must provide either chat_id+message_id or inline_message_id")
        
        if parse_mode:
            data["parse_mode"] = parse_mode
        if reply_markup:
            data["reply_markup"] = reply_markup
        
        result = await self._request("POST", "editMessageText", data)
        return Message(**result)
    
    async def delete_message(
        self,
        chat_id: int,
        message_id: int,
    ) -> bool:
        """Delete message."""
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
        }
        result = await self._request("POST", "deleteMessage", data)
        return result is True
    
    # File methods
    
    async def send_document(
        self,
        chat_id: int,
        document: str,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        reply_markup: Optional[Dict[str, Any]] = None,
    ) -> Message:
        """Send document."""
        data = {
            "chat_id": chat_id,
            "document": document,
        }
        if caption:
            data["caption"] = caption
        if parse_mode:
            data["parse_mode"] = parse_mode
        if reply_markup:
            data["reply_markup"] = reply_markup
        
        result = await self._request("POST", "sendDocument", data)
        return Message(**result)
    
    async def send_photo(
        self,
        chat_id: int,
        photo: str,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        reply_markup: Optional[Dict[str, Any]] = None,
    ) -> Message:
        """Send photo."""
        data = {
            "chat_id": chat_id,
            "photo": photo,
        }
        if caption:
            data["caption"] = caption
        if parse_mode:
            data["parse_mode"] = parse_mode
        if reply_markup:
            data["reply_markup"] = reply_markup
        
        result = await self._request("POST", "sendPhoto", data)
        return Message(**result)
    
    async def send_audio(
        self,
        chat_id: int,
        audio: str,
        caption: Optional[str] = None,
        duration: Optional[int] = None,
        performer: Optional[str] = None,
        title: Optional[str] = None,
        reply_markup: Optional[Dict[str, Any]] = None,
    ) -> Message:
        """Send audio."""
        data = {
            "chat_id": chat_id,
            "audio": audio,
        }
        if caption:
            data["caption"] = caption
        if duration:
            data["duration"] = duration
        if performer:
            data["performer"] = performer
        if title:
            data["title"] = title
        if reply_markup:
            data["reply_markup"] = reply_markup
        
        result = await self._request("POST", "sendAudio", data)
        return Message(**result)
    
    async def send_video(
        self,
        chat_id: int,
        video: str,
        duration: Optional[int] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        reply_markup: Optional[Dict[str, Any]] = None,
    ) -> Message:
        """Send video."""
        data = {
            "chat_id": chat_id,
            "video": video,
        }
        if duration:
            data["duration"] = duration
        if caption:
            data["caption"] = caption
        if parse_mode:
            data["parse_mode"] = parse_mode
        if reply_markup:
            data["reply_markup"] = reply_markup
        
        result = await self._request("POST", "sendVideo", data)
        return Message(**result)
    
    async def get_file(self, file_id: str) -> File:
        """Get file info."""
        data = {"file_id": file_id}
        result = await self._request("POST", "getFile", data)
        return File(**result)
    
    async def get_file_url(self, file_id: str) -> str:
        """Get file URL for downloading."""
        file_info = await self.get_file(file_id)
        if not file_info.file_path:
            raise ValidationException("File path not available")
        return f"{self.BASE_URL}/file/bot{self.token}/{file_info.file_path}"
    
    # User methods
    
    async def get_me(self) -> User:
        """Get bot info."""
        result = await self._request("GET", "getMe")
        return User(**result)
    
    async def get_user_profile_photos(
        self,
        user_id: int,
        offset: int = 0,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """Get user profile photos."""
        data = {
            "user_id": user_id,
            "offset": offset,
            "limit": limit,
        }
        result = await self._request("GET", "getUserProfilePhotos", data)
        return result.get("photos", [])
    
    # Callback query methods
    
    async def answer_callback_query(
        self,
        callback_query_id: str,
        text: Optional[str] = None,
        show_alert: bool = False,
        url: Optional[str] = None,
        cache_time: int = 0,
    ) -> bool:
        """Answer callback query."""
        data = {
            "callback_query_id": callback_query_id,
        }
        if text:
            data["text"] = text
        if show_alert:
            data["show_alert"] = True
        if url:
            data["url"] = url
        if cache_time > 0:
            data["cache_time"] = cache_time
        
        result = await self._request("POST", "answerCallbackQuery", data)
        return result is True
    
    # Chat methods
    
    async def get_chat(self, chat_id: int) -> Dict[str, Any]:
        """Get chat info."""
        data = {"chat_id": chat_id}
        result = await self._request("GET", "getChat", data)
        return result
    
    async def get_chat_member(self, chat_id: int, user_id: int) -> Dict[str, Any]:
        """Get chat member info."""
        data = {
            "chat_id": chat_id,
            "user_id": user_id,
        }
        result = await self._request("GET", "getChatMember", data)
        return result
    
    async def get_chat_members_count(self, chat_id: int) -> int:
        """Get chat members count."""
        data = {"chat_id": chat_id}
        result = await self._request("GET", "getChatMembersCount", data)
        return result
    
    # Update methods
    
    async def get_updates(
        self,
        offset: Optional[int] = None,
        limit: int = 100,
        timeout: int = 30,
        allowed_updates: Optional[List[str]] = None,
    ) -> List[Update]:
        """Get updates via long polling."""
        data = {
            "limit": limit,
            "timeout": timeout,
        }
        if offset is not None:
            data["offset"] = offset
        if allowed_updates:
            data["allowed_updates"] = allowed_updates
        
        result = await self._request("GET", "getUpdates", data)
        return [Update(**item) for item in result]
    
    async def set_webhook(
        self,
        url: str,
        certificate: Optional[str] = None,
        ip_address: Optional[str] = None,
        max_connections: int = 40,
        allowed_updates: Optional[List[str]] = None,
    ) -> bool:
        """Set webhook URL."""
        data = {
            "url": url,
            "max_connections": max_connections,
        }
        if certificate:
            data["certificate"] = certificate
        if ip_address:
            data["ip_address"] = ip_address
        if allowed_updates:
            data["allowed_updates"] = allowed_updates
        
        result = await self._request("POST", "setWebhook", data)
        return result is True
    
    async def delete_webhook(self) -> bool:
        """Delete webhook."""
        result = await self._request("POST", "deleteWebhook", {})
        return result is True
    
    async def get_webhook_info(self) -> Dict[str, Any]:
        """Get webhook info."""
        result = await self._request("GET", "getWebhookInfo")
        return result
