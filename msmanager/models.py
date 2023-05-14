from pydantic import BaseModel
from typing import List

class MindustryServerConfig(BaseModel):
    screen_name: str
    work_dirpath: str
    executable_filepath: str
    arguments: List[str]

class MainConfig(BaseModel):
    servers: List[MindustryServerConfig] = []