from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class Message(BaseModel):
    id: Optional[int]
    body: str
    bookmark: bool = False
    created_at: datetime = datetime.now()
