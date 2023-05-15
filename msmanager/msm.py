import os
from typing import Optional
# * Local Imports
from .config import MSManagerConfig
from .models import MindustryServerConfig
from .units import CONFIG_PATH

class MSManager:
    def __init__(self, config_path: str=CONFIG_PATH) -> None:
        self.config_path = config_path
        
        # * Create children directions
        os.makedirs(os.path.dirname(self.config_path), mode=644, exist_ok=True)

        # * Init Config
        self.config = MSManagerConfig(self.config_path)
    
    # ? Config Managemant
    def add_server_config(self, server: MindustryServerConfig) -> None: self.config.add_server(server)
    def get_server_config(self, screen_name: str) -> Optional[MindustryServerConfig]: self.config.get_server(screen_name)
    def exists_server_config(self, screen_name: str) -> bool: self.config.exists_server(screen_name)
    def remove_server_config(self, screen_name: str) -> None: self.config.remove_server(screen_name)

    
