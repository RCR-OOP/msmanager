import platform
from subprocess import getstatusoutput
from typing import Callable
from .units import SUPPORT_PLATFORMS
from .exceptions import PlatformSupportError, ScreenNotWorkingError

# ! System Functions
def exists_screen() -> bool:
    return getstatusoutput("screen -v")[0] == 0

def get_platform_tag() -> str:
    return f"{platform.system()}-{platform.machine()}".lower()

def checking_platform() -> None:
    if (tag:=get_platform_tag()) not in SUPPORT_PLATFORMS:
        raise PlatformSupportError(tag)
    if not exists_screen():
        raise ScreenNotWorkingError()
