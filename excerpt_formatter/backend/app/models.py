from dataclasses import dataclass
from datetime import time
from typing import Optional

from pydantic import BaseModel


@dataclass
class FormattedInput:
    excerpt_number: int
    text: str
    word_count: int


class FormatterRequest(BaseModel):
    offset_time: Optional[time] = None
    preserve_paragraphs: Optional[bool] = None
    segment_count: Optional[str] = None
    text: str


class MessageRequest(BaseModel):
    slack_api_key: str
    channel_id: str
    excerpt_number: Optional[str] = None
    text: str
    word_count: Optional[str] = None
