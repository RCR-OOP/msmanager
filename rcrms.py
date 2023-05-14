import os
import json
import click
import screens
from typing import List, Any, Iterable, Optional
from pydantic import BaseModel

# ! Constants
LOCALDIR_PATH = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(LOCALDIR_PATH, "rcrms-config.json")

# ! Functions
def json_dump(data: Any, filepath: str) -> None:
    with open(filepath, 'w') as jsonfile:
        json.dump(data, jsonfile)

def json_load(filepath: str) -> Any:
    with open(filepath, 'r') as jsonfile:
        return json.load(jsonfile)

def writefile(__s: str, __filepath: str) -> None:
    with open(__filepath, 'w') as jsonfile:
        jsonfile.write(__s)

# ! Config Types
class ConfigMindustryServer(BaseModel):
    screen_name: str
    executable: str
    args: List[str]

class ConfigRCRMS(BaseModel):
    servers: List[ConfigMindustryServer] = []

class ConfigManager:
    def __init__(self, config_path: str) -> None:
        self.name = config_path
        try:
            self.config = ConfigRCRMS.parse_file(CONFIG_PATH)
        except:
            writefile(ConfigRCRMS().json(), CONFIG_PATH)
            self.config = ConfigRCRMS.parse_file(CONFIG_PATH)
    
    def refresh(self) -> None: writefile(self.config.json(), CONFIG_PATH)
    
    def get_server(self, screen_name: str) -> Optional[ConfigMindustryServer]:
        for i in self.config.servers:
            if i.screen_name == screen_name:
                return i
    
    def exists_server(self, screen_name: str) -> bool:
        return self.get_server(screen_name) is not None
    
    def add_server(self, server: ConfigMindustryServer) -> None:
        if self.exists_server(server.screen_name):
            self.config.servers.append(server)

# ! Config
config_manager = ConfigManager(CONFIG_PATH)

# ! Add Command
@click.command("add", help="Add server in rcrms.")
@click.argument("screen_name", type=str)
@click.argument("executable", type=click.Path(exists=True))
@click.option(
    "-a", "--arg",
    type=str,
    help="The argument to be entered into the executable.",
    multiple=True
)
def add_server(screen_name: str, executable: str, arg: Iterable[str]):
    config_manager.add_server(ConfigMindustryServer(screen_name=screen_name, executable=os.path.abspath(executable), args=list(arg)))
    config_manager.refresh()

# ! Start Command
@click.command("start", help="Start server.")
@click.argument("screen_name", type=str)
def start_server(screen_name: str):
    if (server:=config_manager.get_server(screen_name)) is not None:
        if not screens.exists_session(screen_name):
            session = screens.ScreenSession(screen_name)
            workdir_path = os.path.dirname(server.executable)
            command = " ".join(["java", "-jar", os.path.basename(server.executable), *server.args])
            session.send_command(f"cd {workdir_path}; {command}")

# ! Group
@click.group()
def main():
    pass

# ! Group Init
main.add_command(add_server)
main.add_command(start_server)

# ! Start
if __name__ == '__main__':
    main()