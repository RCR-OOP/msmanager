import os
import click
from rich.console import Console
from typing import Iterable, Optional, Callable, Any
# > Local Imports
from .units import (
    __version__ as prog_version,
    __title__ as prog_name
)
from .msm import MSManager
from .models import MindustryServerConfig
from .functions import (
    rich_exception,
    is_server_connect_correct,
    wait_start_server,
    ping, endicext, parse_connect_data
)
from .exceptions import (
    VBMLParseError, IncorrectConnectionDataError
)

# ! Vars
console = Console()
debag_mode = False
msmanager: MSManager = ...

# ! Functions
def printexcept(e: Exception):
    if debag_mode:
        console.print_exception(word_wrap=True, show_locals=True)
    else:
        console.print(rich_exception(e))

def hand_exception():
    def hand_exception_wrapper(func: Callable[..., Any]):
        def hand_exception_wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                printexcept(e)
        return hand_exception_wrapped
    return hand_exception_wrapper

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
@hand_exception()
def adder(
    screen_name: str,
    executable_filepath: str,
    arguments: Iterable[str],
    host: Optional[str],
    port: Optional[int],
    input_port: Optional[int]
):
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

# ? Remove Command
@click.command("remove", help="Remove the server from the config.")
@click.argument("screen_name", type=str)
@hand_exception()
def remover(screen_name: str):
    msmanager.remove_server_config(screen_name)
    console.print("[green]>[/] Server [bold yellow]removed[/]!")

# ? Start Command
@click.command("start", help="Run the server.")
@click.argument("scn", type=str)
@click.option(
    "-w", "--wait", "wait",
    help="Waiting for the server to start up.",
    is_flag=True
)
@hand_exception()
def starter(scn: str, wait: bool):
    screens_names = scn.split(",")
    for screen_name in screens_names:
        msmanager.start_server(screen_name)
        if (server_config:=msmanager.get_server_config(screen_name)) is not None:
            if is_server_connect_correct(server_config.host, server_config.port, server_config.input_port) and wait:
                wait_start_server(server_config.host, server_config.port, server_config.input_port)
        console.print(f"[green]>[/green] Server [green]{screen_name}[/green] is [bold yellow]started[/bold yellow]!")

# ? Stop Command
@click.command("stop", help="Stop the server.")
@click.argument("scn", type=str)
@hand_exception()
def stoper(scn: str):
    screens_names = scn.split(",")
    for screen_name in screens_names:
        msmanager.stop_server(screen_name)
        console.print(f"[green]>[/green] Server [green]{screen_name}[/green] is [bold yellow]stoped[/bold yellow]!")

# ? List Command
@click.command("list", help="List of servers in the config.")
@click.option(
    "--pinging", "pinging",
    help="Whether to do a ping to check.",
    is_flag=True, default=False
)
@click.option(
    "-t", "--timeout", "timeout",
    help="Maximum response waiting time (in seconds).",
    type=int, default=10, show_default=True
)
@hand_exception()
def lister(pinging: bool, timeout: int):
    try:
        if len(msmanager.config.config.servers) != 0:
            for idx, server in enumerate(msmanager.config.config.servers):
                lines = [
                    f"({idx}) Server {repr(server.screen_name)}:",
                    f"[magenta]Executable Filepath[/] : {repr(server.executable_filepath)}",
                    f"[magenta]Arguments[/]           : {repr(server.arguments)}",
                    f"[magenta]Host[/]                : [green]{server.host}[/]",
                    f"[magenta]Port[/]                : [cyan]{server.port}[/]",
                    f"[magenta]Input Port[/]          : [cyan]{server.input_port}[/]"
                ]
                if pinging:
                    try:
                        ping(server.host, server.port, timeout)
                        started = True
                    except:
                        started = False
                    lines.append(f"[magenta]Started[/]             : {repr(started)}")
                console.print("\n\t".join(lines))
        else:
            console.print("[green]>[/] The list of servers is [bold yellow]empty[/]!")
    except Exception as e:
        console.print(rich_exception(e))

@click.command("ping", help="Server status check.")
@click.argument("connect", type=str)
@click.option(
    "-t", "--timeout", "timeout",
    help="Maximum response waiting time (in seconds).",
    type=int, default=10, show_default=True
)
@hand_exception()
def pinger(connect: str, timeout: int):
    if (server_config:=msmanager.get_server_config(connect)) is not None:
        connect_data = {"host": server_config.host, "port": server_config.port}
    else:
        try:
            connect_data = parse_connect_data(connect)
        except VBMLParseError:
            raise IncorrectConnectionDataError(connect)
    status = ping(connect_data["host"], connect_data["port"], timeout)
    console.print(
        "\n\t".join(
            [
                f"[green]>[/] Server {endicext(status.name)}:",
                f"- [magenta]Players[/] : {status.players} players",
                f"- [magenta]Map[/]     : {repr(status.map)}",
                f"- [magenta]Wave[/]    : {status.wave} wave",
                f"- [magenta]Ping[/]    : {round(status.ping)} ms",
                f"- [magenta]Version[/] : {repr(status.version)}",
                f"- [magenta]Vertype[/] : {repr(status.vertype)}"
            ]
        )
    )

# ! Main Group
@click.group()
@click.option(
    "-nce", "--not-check-environment", "not_check_environment",
    help="Disables checks for GNU Screen, Java and system support.",
    is_flag=True
)
@click.option(
    "--debug", "-d", "debug",
    help="Enables debug mode of operation.",
    is_flag=True
)
@click.version_option(
    version=prog_version,
    prog_name=prog_name
)
@hand_exception()
def main(not_check_environment: bool, debug: bool):
    global msmanager, debag_mode
    
    debag_mode = debug
    
    msmanager = MSManager(check_environment=(not not_check_environment))

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