from pydantic import BaseModel
from typing import List

class MindustryServer(BaseModel):
    screen_name: str
    work_dirpath: str
    executable_filepath: str
    arguments: List[str]

class MainConfig(BaseModel):
    servers: List[MindustryServer] = []