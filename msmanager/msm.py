import os
from typing import Optional
from versioner import Version
# * Local Imports
from .units import CONFIG_PATH
from .config import MSManagerConfig
from .models import MindustryServerConfig
from .functions import get_mindustry_server_version, checking_environment
from .exceptions import ServerNotExistsError

class MSManager:
    def __init__(self, config_path: str=CONFIG_PATH) -> None:
        self.config_path = config_path
        
        # * Create children directions
        os.makedirs(os.path.dirname(self.config_path), mode=644, exist_ok=True)

        # * Init Config
        self.config = MSManagerConfig(self.config_path)

        # * Test System
        checking_environment()
    
    # ? Config Managemant
    def add_server_config(self, server: MindustryServerConfig) -> None: self.config.add_server(server)
    def get_server_config(self, screen_name: str) -> Optional[MindustryServerConfig]: self.config.get_server(screen_name)
    def exists_server_config(self, screen_name: str) -> bool: self.config.exists_server(screen_name)
    def remove_server_config(self, screen_name: str) -> None: self.config.remove_server(screen_name)

    # ? ...
    def check_server_version(self, screen_name: str) -> Version:
        if (server_config:=self.get_server_config(screen_name)) is not None:
            return get_mindustry_server_version(server_config.executable_filepath)
        raise ServerNotExistsError(screen_name)
            