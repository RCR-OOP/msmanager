import os
import click
from rich.console import Console
from typing import Iterable, Optional
# > Local Imports
from .msm import MSManager
from .models import MindustryServerConfig
from .functions import (
    rich_exception,
    is_server_connect_correct,
    wait_start_server,
    ping, endicext
)

# ! Vars
console = Console()
msmanager: MSManager = ...

# ! Commands
# ? Add Command
@click.command("add", help="Add a server to the config.")
@click.argument("screen_name", type=str)
@click.argument("executable_filepath", type=click.Path(exists=True))
@click.option(
    "-a", "--arg", "arguments",
    help="Arguments for starting a server.",
    type=str,
    multiple=True
)
@click.option(
    "-h", "--host", "host",
    help="Server connection host.",
    type=str, default=None, show_default=True
)
@click.option(
    "-p", "--port", "port",
    help="Server connection port.",
    type=int, default=None, show_default=True
)
@click.option(
    "-i", "--input-port", "input_port",
    help="Server input port for telnet connection.",
    type=int, default=None, show_default=True
)
def adder(
    screen_name: str,
    executable_filepath: str,
    arguments: Iterable[str],
    host: Optional[str],
    port: Optional[int],
    input_port: Optional[int]
):
    try:
        msmanager.add_server_config(
            MindustryServerConfig(
                screen_name=screen_name,
                work_dirpath=os.path.dirname(os.path.abspath(executable_filepath)),
                executable_filepath=os.path.abspath(executable_filepath),
                arguments=list(arguments),
                host=host, port=port, input_port=input_port
            )
        )
        console.print("[green]>[/] Server [bold yellow]added[/]!")
    except Exception as e:
        console.print(rich_exception(e))

# ? Remove Command
@click.command("remove", help="Remove the server from the config.")
@click.argument("screen_name", type=str)
def remover(screen_name: str):
    try:
        msmanager.remove_server_config(screen_name)
        console.print("[green]>[/] Server [bold yellow]removed[/]!")
    except Exception as e:
        console.print(rich_exception(e))

# ? Start Command
@click.command("start", help="Run the server.")
@click.argument("screen_name", type=str)
@click.option("-w", "--wait", "wait", is_flag=True, help="Waiting for the server to start up.")
def starter(screen_name: str, wait: bool):
    try:
        msmanager.start_server(screen_name)
        if (server_config:=msmanager.get_server_config(screen_name)) is not None:
            if is_server_connect_correct(server_config.host, server_config.port, server_config.input_port) and wait:
                wait_start_server(server_config.host, server_config.port, server_config.input_port)
        console.print("[green]>[/] Server [bold yellow]started[/]!")
    except Exception as e:
        console.print(rich_exception(e))

# ? Stop Command
@click.command("stop", help="Stop the server.")
@click.argument("screen_name", type=str)
def stoper(screen_name: str):
    try:
        msmanager.stop_server(screen_name)
        console.print("[green]>[/] Server [bold yellow]stoped[/]!")
    except Exception as e:
        console.print(rich_exception(e))

# ? List Command
@click.command("list", help="List of servers in the config.")
def lister():
    try:
        if len(msmanager.config.config.servers) != 0:
            for idx, server in enumerate(msmanager.config.config.servers):
                console.print(
                    "\n\t".join(
                        [
                            f"({idx}) Server [green]{server.screen_name}[/]:",
                            f"[yellow]EXECUTABLE_FILEPATH[/]  : {repr(server.executable_filepath)}",
                            f"[yellow]ARGUMENTS[/]            : {repr(' '.join(server.arguments))}",
                            f"[yellow]HOST:PORT:INPUT_PORT[/] : [green]{server.host}[/]:{server.port}:{server.input_port}"
                        ]
                    )
                )
        else:
            console.print("[green]>[/] The list of servers is [bold yellow]empty[/]!")
    except Exception as e:
        console.print(rich_exception(e))

@click.command("ping", help="Server status check.")
@click.argument("host", type=str)
@click.argument("port", type=int)
@click.option(
    "-t", "--timeout", "timeout",
    help="Maximum response waiting time (in seconds).",
    type=int, default=10, show_default=True
)
def pinger(host: str, port: int, timeout: int):
    try:
        status = ping(host, port, timeout)
        console.print(
            "\n\t".join(
                [
                    f"[green]>[/] Server {endicext(status.name)}:",
                    f"- [yellow]Players[/] : {status.players} players",
                    f"- [yellow]Map[/]     : [green]{status.map}[/]",
                    f"- [yellow]Wave[/]    : {status.wave} wave",
                    f"- [yellow]Ping[/]    : {round(status.ping)} ms",
                    f"- [yellow]Version[/] : [green]v{status.version}[/]",
                    f"- [yellow]Vertype[/] : [green]{status.vertype}[/]"                    
                ]
            )
        )
    except Exception as e:
        console.print(rich_exception(e))

# ! Main Group
@click.group()
@click.option(
    "-nce", "--not-check-environment", "not_check_environment",
    is_flag=True,
    help="Disables checks for GNU Screen, Java and system support."
)
def main(not_check_environment: bool):
    global msmanager
    msmanager = MSManager(
        check_environment=(not not_check_environment)
    )

# ! Add in Group
main.add_command(adder)
main.add_command(remover)
main.add_command(starter)
main.add_command(stoper)
main.add_command(lister)
main.add_command(pinger)

# ! Run
def run():
    main()