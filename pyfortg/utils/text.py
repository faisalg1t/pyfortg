"""Text processing utilities."""

import re
from typing import Tuple, Optional


def escape_html(text: str) -> str:
    """Escape HTML special characters."""
    replacements = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def escape_markdown(text: str) -> str:
    """Escape Markdown special characters."""
    special_chars = r'\_*[]()~`>#+-=|{}.!'
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text


def escape_markdown_v2(text: str) -> str:
    """Escape Markdown V2 special characters."""
    special_chars = r'_*[]()~`>#+-=|{}.!'
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text


def parse_command(text: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Parse command from message text.
    
    Args:
        text: Message text
    
    Returns:
        Tuple of (command, args) or (None, None) if not a command
    """
    if not text or not text.startswith('/'):
        return None, None
    
    parts = text.split(maxsplit=1)
    command = parts[0][1:].split('@')[0]  # Remove / and bot mention
    args = parts[1] if len(parts) > 1 else None
    
    return command, args


def extract_command(text: str) -> Optional[str]:
    """Extract command from message text."""
    command, _ = parse_command(text)
    return command


def extract_command_args(text: str) -> Optional[str]:
    """Extract command arguments from message text."""
    _, args = parse_command(text)
    return args


def is_command(text: str) -> bool:
    """Check if message text is a command."""
    return text.startswith('/') if text else False


def extract_entities(text: str, entities: list) -> dict:
    """
    Extract entities from message.
    
    Args:
        text: Message text
        entities: List of entity dicts with offset, length, type
    
    Returns:
        Dictionary with entity type as key and list of extracted text as value
    """
    result = {}
    
    for entity in entities:
        offset = entity.get('offset', 0)
        length = entity.get('length', 0)
        entity_type = entity.get('type', 'unknown')
        
        extracted_text = text[offset:offset + length]
        
        if entity_type not in result:
            result[entity_type] = []
        result[entity_type].append(extracted_text)
    
    return result


def extract_hashtags(text: str) -> list:
    """Extract hashtags from text."""
    pattern = r'#\w+'
    return re.findall(pattern, text)


def extract_mentions(text: str) -> list:
    """Extract @mentions from text."""
    pattern = r'@\w+'
    return re.findall(pattern, text)


def extract_urls(text: str) -> list:
    """Extract URLs from text."""
    pattern = r'https?://\S+'
    return re.findall(pattern, text)


def extract_emails(text: str) -> list:
    """Extract email addresses from text."""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(pattern, text)


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def bold(text: str) -> str:
    """Format text as bold in HTML."""
    return f"<b>{escape_html(text)}</b>"


def italic(text: str) -> str:
    """Format text as italic in HTML."""
    return f"<i>{escape_html(text)}</i>"


def code(text: str) -> str:
    """Format text as code in HTML."""
    return f"<code>{escape_html(text)}</code>"


def pre(text: str, language: str = "") -> str:
    """Format text as preformatted in HTML."""
    return f"<pre><code class='{language}'>{escape_html(text)}</code></pre>"
