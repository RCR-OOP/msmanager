from .units import SUPPORT_PLATFORMS

class PlatformSupportError(Exception):
    """Indicates that the `Screen (GNU)` is not working correctly or is missing."""
    def __init__(self, currect_platform: str) -> None:
        """Called if the program cannot work with the current platform."""
        self.args = (
            "Your platform ({0}) is not supported, only the following platforms are supported: {1}".format(
                repr(currect_platform), ", ".join([repr(i) for i in SUPPORT_PLATFORMS])
            ),
        )

class ScreenNotWorkingError(Exception):
    """Indicates problems with the `GNU Screen`."""
    def __init__(self) -> None:
        """Called if there are problems when trying to work with `GNU Screen`."""
        self.args = (
            """The screen command returns an error when checked, check that the 'GNU Screen' program is working. \nIf the software is not available, the following program must be installed: https://www.gnu.org/software/screen""",
        )