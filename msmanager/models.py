from pydantic import BaseModel
from typing import List, Optional

class MindustryServerConfig(BaseModel):
    screen_name: str
    work_dirpath: str
    executable_filepath: str
    arguments: List[str]
    host: Optional[str]=None
    port: Optional[int]=None
    input_port: Optional[int]=None

class MainConfig(BaseModel):
    servers: List[MindustryServerConfig] = []