import time
import pydustry
import platform
from versioner import Version
from vbml import Pattern, Patcher
from subprocess import getstatusoutput
from typing import Tuple, Dict, Any, Iterable
# * Local Imports
from .types import DefaultVersioner, DefaultVBMLPacther
from .units import SUPPORT_PLATFORMS, COLORS_STRINGS_REPLACEBLE
from .exceptions import (
    VBMLParseError, 
    PlatformSupportError,
    ScreenNotWorkingError,
    JavaNotFound
)

# ! Standart Functions
def replaces(string: str, replaceble: Dict[str, str]) -> str:
    for __old, __new in replaceble.items():
        string = string.replace(__old, __new)
    return string

def rich_exception(exception: Exception) -> str:
    return f"[red]{exception.__class__.__name__}:[/] {' '.join(exception.args)}"

# ! ...
def wait_start_server(
    server_host: str,
    port: int=6567,
    input_port: int=6859,
    per_second: float=1
) -> None:
    server = pydustry.Server(server_host, port, input_port)
    while True:
        try:
            server.get_status(per_second)
            break
        except:
            pass

def is_server_connect_correct(server_host: str, port: int, input_port: int) -> bool:
    return isinstance(server_host, str) and isinstance(port, int) and isinstance(input_port, int)

# ! Subproccess Functions
def runner(*args: str) -> Tuple[int, str]:
    return getstatusoutput(" ".join([*args]))

def exists_screen() -> bool:
    return runner("screen", "-v")[0] == 0

def exists_java() -> bool:
    return runner("java", "--version")[0] == 0

# ! Parse Functions
def remove_color(text: str) -> str:
    return replaces(text, COLORS_STRINGS_REPLACEBLE)

def parse_vbml(text: str, pattern: str, *, pacther: Patcher=DefaultVBMLPacther) -> Dict[str, Any]:
    data = pacther.check(Pattern(pattern), text)
    if isinstance(data, dict):
        return data
    raise VBMLParseError()

def parse_vbml_linear(lines: Iterable[str], pattern: str, *, pacther: Patcher=DefaultVBMLPacther) -> Dict[str, Any]:
    for line in lines:
        try: return parse_vbml(line, pattern, pacther=pacther)
        except: pass
    raise VBMLParseError()

def get_java_version() -> Version:
    if exists_java():
        data = parse_vbml(runner("java", "--version")[1].split("\n")[0], "<t1> <version> <t2>")
        return DefaultVersioner.parse(data["version"])
    raise JavaNotFound()

def get_mindustry_server_version(jarfilepath: str) -> Version:
    if exists_java():
        text = runner("java", "-jar", f"\"{jarfilepath}\"", "version,exit")[1]
        lines = [ remove_color(i) for i in text.split("\n") ]
        data = parse_vbml_linear(lines, "<dt> [I] Version: <build> / build <version>")
        return DefaultVersioner.parse(data["version"])
    raise JavaNotFound()

# ! System Functions
def get_platform_tag() -> str:
    return f"{platform.system()}-{platform.machine()}".lower()

def checking_environment() -> None:
    if (tag:=get_platform_tag()) not in SUPPORT_PLATFORMS:
        raise PlatformSupportError(tag)
    if not exists_screen():
        raise ScreenNotWorkingError()
    if not exists_java():
        raise JavaNotFound()
