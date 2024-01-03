import os
import json
import click
from rich.console import Console
from typing import Literal, Optional, Union, Iterable, Callable, Dict, Any
# > Local Imports
from .msm import MSManager
from .units import (
    __title__ as prog_name,
    __version__ as prog_version
)
from .models import (
    MindustryServerConfig,
    JsonOutput
)
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
oformat: Literal['text', 'json'] = 'text'

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
                if oformat == 'text':
                    printexcept(e)
                elif oformat == 'json':
                    printjson(
                        JsonOutput(
                            status='error',
                            data={
                                'name': e.__class__.__name__,
                                'args': list(e.args),
                                'kwargs': {}
                            }
                        )
                    )
        return hand_exception_wrapped
    return hand_exception_wrapper

def printjson(data: Union[Dict[str, Any], JsonOutput]) -> None:
    if isinstance(data, JsonOutput):
        print(data.model_dump_json(warnings=False))
    elif isinstance(data, dict):
        print(json.dumps(data))
    else:
        raise TypeError(data)

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
    if oformat == 'text':
        console.print("[green]>[/] Server [bold yellow]added[/]!")
    elif oformat == 'json':
        printjson(JsonOutput(status='success'))

# ? Remove Command
@click.command("remove", help="Remove the server from the config.")
@click.argument("screen_name", type=str)
@hand_exception()
def remover(screen_name: str):
    msmanager.remove_server_config(screen_name)
    if oformat == 'text':
        console.print("[green]>[/] Server [bold yellow]removed[/]!")
    elif oformat == 'json':
        printjson(JsonOutput(status='success'))

# ? Start Command
@click.command("start", help="Run the server(s).")
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
        if oformat == 'text':
            console.print(f"[green]>[/green] Server [green]{screen_name}[/green] is [bold yellow]started[/bold yellow]!")
    if oformat == 'json':
        printjson(JsonOutput(status='success'))

# ? Stop Command
@click.command("stop", help="Stop the server(s).")
@click.argument("scn", type=str)
@hand_exception()
def stoper(scn: str):
    screens_names = scn.split(",")
    for screen_name in screens_names:
        msmanager.stop_server(screen_name)
        if oformat == 'text':
            console.print(f"[green]>[/green] Server [green]{screen_name}[/green] is [bold yellow]stoped[/bold yellow]!")
    if oformat == 'json':
        printjson(JsonOutput(status='success'))

@click.command("restart", help="Restart the server(s).")
@click.argument("scn", type=str)
@click.option(
    "-w", "--wait", "wait",
    help="Waiting for the server to start up.",
    is_flag=True
)
@hand_exception()
def restarter(scn: str, wait: bool):
    screens_names = scn.split(",")
    for screen_name in screens_names:
        msmanager.stop_server(screen_name)
        if oformat == 'text':
            console.print(f"[green]>[/green] Server [green]{screen_name}[/green] is [bold yellow]stoped[/bold yellow]!")
    for screen_name in screens_names:
        msmanager.start_server(screen_name)
        if (server_config:=msmanager.get_server_config(screen_name)) is not None:
            if is_server_connect_correct(server_config.host, server_config.port, server_config.input_port) and wait:
                wait_start_server(server_config.host, server_config.port, server_config.input_port)
        if oformat == 'text':
            console.print(f"[green]>[/green] Server [green]{screen_name}[/green] is [bold yellow]started[/bold yellow]!")
    if oformat == 'json':
        printjson(JsonOutput(status='success'))

# ? List Command
@click.command("list", help="List of servers in the config.")
@click.option(
    "--pinging", "-p", "pinging",
    help="Whether to do a ping to check.",
    is_flag=True, default=False
)
@click.option(
    "--timeout", "-t", "timeout",
    help="Maximum response waiting time (in seconds).",
    type=int, default=10, show_default=True
)
@hand_exception()
def lister(pinging: bool, timeout: int):
    if oformat == 'json':
        output = JsonOutput(status='success', data={"servers": []})
    if len(msmanager.config.config.servers) != 0:
        for idx, server in enumerate(msmanager.config.config.servers):
            if oformat == 'text':
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
                if oformat == 'text':
                    lines.append(f"[magenta]Started[/]             : {repr(started)}")
            if oformat == 'text':
                console.print("\n\t".join(lines))
            if oformat == 'json':
                output.data['servers'].append(
                    {
                        "executable_filepath": server.executable_filepath,
                        "arguments": server.arguments,
                        "host": server.host,
                        "port": server.port,
                        "input_port": server.input_port,
                        "started": started
                    }
                )
    else:
        if oformat == 'text':
            console.print("[green]>[/] The list of servers is [bold yellow]empty[/]!")
    if oformat == 'json':
        printjson(output)

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
            if oformat == 'text':
                raise IncorrectConnectionDataError(connect)
            elif oformat == 'json':
                printjson(
                    JsonOutput(
                        status='error',
                        data={
                            'name': 'IncorrectConnectionDataError',
                            'args': [connect],
                            'kwargs': {}
                        }
                    )
                )
    status = ping(connect_data["host"], connect_data["port"], timeout)
    if oformat == 'text':
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
    elif oformat == 'json':
        printjson(
            JsonOutput(
                status='success',
                data={
                    "name": status.name,
                    "players": status.players,
                    "map": status.map,
                    "wave": status.wave,
                    "ping": status.ping,
                    "version": status.version,
                    "vertype": status.vertype
                }
            )
        )

# ! Main Group
@click.group()
@click.option(
    "--check-environment", "check_environment",
    help="Enables checks for GNU Screen, Java and system support.",
    is_flag=True, default=False
)
@click.option(
    "--debug", "-d", "debug",
    help="Enables debug mode of operation.",
    is_flag=True
)
@click.option(
    "--format", "-f", "output_format",
    help="The output format.", type=click.Choice(['text', 'json']),
    default="text", show_default=True
)
@click.version_option(
    version=prog_version,
    prog_name=prog_name
)
@hand_exception()
def main(
    check_environment: bool,
    debug: bool,
    output_format: Literal['text', 'json']
):
    global msmanager, debag_mode, oformat
    debag_mode, oformat = debug, output_format
    msmanager = MSManager(check_environment=check_environment)

# ! Add in Group
main.add_command(adder)
main.add_command(remover)
main.add_command(starter)
main.add_command(stoper)
main.add_command(restarter)
main.add_command(lister)
main.add_command(pinger)

# ! Run
def run():
    main()