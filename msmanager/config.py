import os
from pathlib import Path
from typing import Optional
from .models import MainConfig, MindustryServerConfig
from .exceptions import (
    ServerExistsError, ServerNotExistsError
)

# ! Config Manager
class MSManagerConfig:
    @staticmethod
    def load(filepath: str) -> MainConfig:
        return MainConfig.parse_file(filepath)
    
    @staticmethod
    def dump(filepath: str, data: MainConfig) -> None:
        with open(filepath, "w") as file:
            file.write(data.json())
    
    def refresh(self) -> None: self.dump(self.name, self.config)
    
    def __init__(self, config_path: str) -> None:
        self.name = os.path.abspath(config_path)
        self.name_path = Path(self.name)
        
        if self.name_path.exists():
            try:
                self.config = self.load(self.name)
            except:
                self.config = MainConfig()
                self.refresh()
        else:
            self.config = MainConfig()
            self.refresh()
    
    def get_server(self, screen_name: str) -> Optional[MindustryServerConfig]:
        for server in self.config.servers:
            if server.screen_name == screen_name:
                return server
    
    def get_server_index(self, screen_name: str) -> Optional[int]:
        for idx, server in enumerate(self.config.servers):
            if server.screen_name == screen_name:
                return idx
    
    def exists_server(self, screen_name: str) -> bool:
        return self.get_server(screen_name) is not None
    
    def add_server(self, server: MindustryServerConfig) -> None:
        if not self.exists_server(server.screen_name):
            self.config.servers.append(server)
            self.refresh()
        else:
            raise ServerExistsError(server.screen_name)
    
    def remove_server(self, screen_name: str) -> None:
        if (server_index:=self.get_server_index(screen_name)) is not None:
            self.config.servers.pop(server_index)
            self.refresh()
        else:
            raise ServerNotExistsError(screen_name)