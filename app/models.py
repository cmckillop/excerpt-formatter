from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


@dataclass
class FormattedInput:
    excerpt_number: int
    text: str
    word_count: int


class FormatterRequest(BaseModel):
    date_time: Optional[datetime] = None
    preserve_paragraphs: Optional[bool] = None
    text: str


class MessageRequest(BaseModel):
    slack_api_key: str
    channel_id: str
    excerpt_number: Optional[str] = None
    text: str
    word_count: Optional[str] = None
