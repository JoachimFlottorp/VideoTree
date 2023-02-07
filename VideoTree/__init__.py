from dataclasses import dataclass
from typing import List, Optional


@dataclass
class File:
    name: str
    path: str
    time: Optional[int]
    extension: str
    

@dataclass
class Folder:
    name: str
    path: str
    children: List["Folder"]
    files: List["File"]

from .VideoTree import videotree
