from typing import Literal

from pydantic import BaseModel
from pygame import Rect


class DisplayButton(BaseModel, arbitrary_types_allowed=True):
    rect: Rect
    text: str
    btn_type: Literal['floor', 'control']
    floor: int
    pressed: bool = False


class ElevatorState(BaseModel):
    floor: int
    move: Literal['STOP', 'UP', 'DOWN']
