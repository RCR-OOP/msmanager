from pydantic import BaseModel
from typing import Optional, Literal, Dict, List, Any

# ! MSManager Models
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

# ! MSManager Json Output Models
class JsonOutput(BaseModel):
    status: Literal['success', 'error']
    data: Dict[str, Any]={}