import os
import time
import json
import click
import datetime
from rich.console import Console
from typing import Literal, Optional, Union, Iterable, Callable, List, Dict, Any
# > Local Imports
from .msm import MSManager
from .units import (
    __title__ as prog_name,
    __version__ as prog_version,
    ERRORLOG_DIRPATH
)
from .models import (
    MindustryServerConfig,
    JsonOutput
)
from .functions import (
    remove_color,
    rich_exception,
    is_server_connect_correct,
    wait_start_server,
    ping, pingok,
    endicext, parse_connect_data
)
from .exceptions import (
    VBMLParseError, IncorrectConnectionDataError,
    ServerIsStoppedError, ServerIsStartedError
)

# ! Vars
console = Console()
debug_mode = False
verbose_mode = False
msmanager: MSManager = ...
oformat: Literal['text', 'json'] = 'text'

# ! Functions
def print_exception(e: Exception) -> None:
    if debug_mode:
        console.print_exception(word_wrap=True, show_locals=True)
    else:
        console.print(rich_exception(e))

def save_print_exception() -> None:
    cdt = datetime.datetime.now()
    with console.capture() as cap:
        console.print_exception(word_wrap=True, show_locals=True)
    text = remove_color(cap.get())
    with open(os.path.join(ERRORLOG_DIRPATH, "last.log"), "w") as logfile:
        logfile.write(text)
    with open(os.path.join(ERRORLOG_DIRPATH, f"{round(cdt.timestamp())}.log"), "w") as logfile:
        logfile.write(text)

def hand_exception():
    def hand_exception_wrapper(func: Callable[..., Any]):
        def hand_exception_wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if oformat == 'text':
                    print_exception(e)
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
        if (server_config := msmanager.get_server_config(screen_name)) is not None:
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

# ? Restart Command
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
            console.print(f"Server [green]{screen_name}[/green] is [bold yellow]started[/bold yellow]!")
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

# ? Ping Command
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

# ? Watchdog
@click.command("watchdog", help="The active process of monitoring servers, which, if the server fails, restarts it.")
@click.argument("scn", type=str)
@click.option(
    "--localhost", "-l", "localhost", 
    help="The ping will take place not by the host settings, but by the local IP.",
    default=False, is_flag=True
)
@click.option(
    "--start-delay", "-d", "start_delay",
    help="The delay before watchdog starts (in secounds).",
    type=click.INT, default=60, show_default=True
)
@click.option(
    "--check-timeout", "-ct", "check_timeout",
    help="The delay between process checks (in secounds).",
    type=click.INT, default=1, show_default=True
)
@click.option(
    "--checks", "-c", "checks",
    help="How many times to check one server.",
    type=click.INT, default=3, show_default=True
)
@click.option(
    "--all-timeout", "-at", "all_timeout",
    help="Runs a check of all servers once in a while (in secounds).",
    type=click.INT, default=600, show_default=True
)
@hand_exception()
def watchdog(
    scn: str,
    localhost: bool,
    start_delay: int,
    check_timeout: int,
    checks: int,
    all_timeout: int
):
    screens_names = scn.split(",")
    servers_config: List[MindustryServerConfig] = []
    for screen_name in screens_names:
        if (server_config := msmanager.get_server_config(screen_name)) is not None:
            if (server_config.host is not None) or (server_config.port is not None):
                servers_config.append(server_config)
                console.print(f"[green]>[/green] The server was found in the config: {repr(screen_name)}")
            else:
                console.print(f"[red]>[/red] There are no settings for ping: {repr(screen_name)}")
        else:
            console.print(f"[red]>[/red] One of the listed servers was not found: {repr(screen_name)}")
    console.print(f"[green]>[/green] Waiting {start_delay} second(s) before starting the watchdog operation.")
    time.sleep(start_delay)
    console.print("[green]>[/green] Watchdog is started!")
    try:
        while True:
            for server_config in servers_config:
                oks, server_host = 0, "localhost" if localhost else server_config.host
                if verbose_mode:
                    console.print(f"[yellow]>[/yellow] Checking: {repr(server_config.screen_name)}")
                for _ in range(checks):
                    if pingok(server_host, server_config.port):
                        oks += 1
                        if verbose_mode:
                            console.print(f"[yellow]>[/yellow] Checked: [green]ON[/green]")
                    else:
                        if verbose_mode:
                            console.print(f"[yellow]>[/yellow] Checked: [red]OFF[/red]")
                    time.sleep(check_timeout)
                if oks == 0:
                    ok = False
                    while not ok:
                        console.print(f"[red]>[/red] Attempt to restart the server: {repr(server_config.screen_name)}")
                        try:
                            msmanager.stop_server(server_config.screen_name)
                        except ServerIsStoppedError:
                            pass
                        try:
                            msmanager.start_server(server_config.screen_name)
                            wait_start_server(server_config.host, server_config.port, server_config.input_port)
                            ok = True
                        except ServerIsStartedError:
                            save_print_exception()
                            ok = False
                        if ok:
                            console.print(f"[green]>[/green] The server has been restarted: {repr(server_config.screen_name)}")
            time.sleep(all_timeout)
    except KeyboardInterrupt:
        pass
    console.print("[green]>[/green] Watchdog is shutdown!")

# ! Main Group
@click.group()
@click.option(
    "--check-environment", "check_environment",
    help="Enables checks for GNU Screen, Java and system support.",
    is_flag=True, default=False
)

@click.option(
    "--format", "-f", "output_format",
    help="The output format.", type=click.Choice(['text', 'json']),
    default="text", show_default=True
)
@click.option(
    "--debug", "-d", "debug",
    help="Enables debug mode of operation.",
    is_flag=True, default=False
)
@click.option(
    "--verbose", "verbose",
    help="Displaying more detailed logs.",
    is_flag=True, default=False
)
@click.version_option(
    version=prog_version,
    prog_name=prog_name
)
@hand_exception()
def main(
    check_environment: bool,
    output_format: Literal['text', 'json'],
    debug: bool,
    verbose: bool
):
    global msmanager, debug_mode, oformat, verbose_mode
    debug_mode, verbose_mode, oformat = debug, verbose, output_format
    msmanager = MSManager(check_environment=check_environment)

# ! Add in Group
main.add_command(adder)
main.add_command(remover)
main.add_command(starter)
main.add_command(stoper)
main.add_command(restarter)
main.add_command(lister)
main.add_command(pinger)
main.add_command(watchdog)

# ! Run
def run():
    main()