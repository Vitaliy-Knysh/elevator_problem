from pydantic import BaseModel
from typing import Literal

from pygame import Rect


class DisplayButton(BaseModel, arbitrary_types_allowed=True):
    rect: Rect
    text: str
    btn_id: str
    btn_type: Literal['floor', 'control']
    floor: int
    pressed: bool = False
