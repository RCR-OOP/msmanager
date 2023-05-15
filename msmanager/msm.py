import os
import screens
from typing import Optional
from versioner import Version
# * Local Imports
from .units import CONFIG_PATH
from .config import MSManagerConfig
from .models import MindustryServerConfig
from .functions import get_mindustry_server_version, checking_environment
from .exceptions import ServerNotExistsError, ServerIsStartedError, ServerIsStoppedError

class MSManager:
    def __init__(self, config_path: str=CONFIG_PATH, check_environment: bool=True) -> None:
        self.config_path = config_path
        
        # * Create children directions
        os.makedirs(os.path.dirname(self.config_path), mode=644, exist_ok=True)

        # * Init Config
        self.config = MSManagerConfig(self.config_path)

        # * Test System
        if check_environment:
            checking_environment()
    
    # ? Config Managemant
    def add_server_config(self, server: MindustryServerConfig) -> None: self.config.add_server(server)
    def get_server_config(self, screen_name: str) -> Optional[MindustryServerConfig]: self.config.get_server(screen_name)
    def exists_server_config(self, screen_name: str) -> bool: self.config.exists_server(screen_name)
    def remove_server_config(self, screen_name: str) -> None: self.config.remove_server(screen_name)

    # ? Server Managemant
    def check_server_version(self, screen_name: str) -> Version:
        if (server_config:=self.get_server_config(screen_name)) is not None:
            return get_mindustry_server_version(server_config.executable_filepath)
        raise ServerNotExistsError(screen_name)
    
    def server_is_started(self, screen_name: str) -> bool:
        return screens.get_session_by_name(screen_name) is not None
    
    def start_server(self, screen_name: str) -> None:
        server_config = self.get_server_config(screen_name)
        if server_config is not None:
            if not self.server_is_started(screen_name):
                server_screen = screens.Screen(server_config.screen_name)
                args = " ".join(server_config.arguments)
                server_screen.send_command(
                    f"cd {server_config.work_dirpath} ; java -jar {server_config.executable_filepath} {args}"
                )
            else:
                raise ServerIsStartedError(screen_name)
        else:
            raise ServerNotExistsError(screen_name)

    def stop_server(self, screen_name: str) -> None:
        server_config = self.get_server_config(screen_name)
        if server_config is not None:
            server_screen = screens.get_session_by_name(screen_name)
            if server_screen is not None:
                server_screen.kill()
                screens.wipe()
            else:
                raise ServerIsStoppedError(screen_name)
        else:
            raise ServerNotExistsError(screen_name)
    