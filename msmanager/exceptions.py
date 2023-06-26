from .units import SUPPORT_PLATFORMS

# ! System Exceptions
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

class JavaNotFound(Exception):
    """Indicates a lack of `Java`."""
    def __init__(self) -> None:
        """Called if the `Java` package environment could not be found."""
        self.args = ("The `Java` environment package is not installed.",)

# ! Parsing Error
class VBMLParseError(Exception):
    """Indicates a parsing error."""
    def __init__(self) -> None:
        """Calls if `vbml` was unable to finish parsing."""
        self.args = ("There was an error parsing through vbml.",)


# ! Config Exceptions
class ServerExistsError(Exception):
    """Indicates that there is a server with this name."""
    def __init__(self, name: str) -> None:
        """Called if a server with this name is already present in the config."""
        self.args = (f"A server named {repr(name)} already exists in the config.",)

class ServerNotExistsError(Exception):
    """Indicates that north does not exist in the config."""
    def __init__(self, name: str) -> None:
        """Called if a server with this name does not exist in the config."""
        self.args = (
            f"A server named {repr(name)} does not exist in the config."
        )

# ! Server Actions Exceptions
class ServerIsStartedError(Exception):
    """Indicates that the server is already running."""
    def __init__(self, name: str) -> None:
        """Called when attempting to start an already running server."""
        self.args = (
            f"A server named {repr(name)} is already up and running."
        )

class ServerIsStoppedError(Exception):
    """Indicates that the server is already stopped."""
    def __init__(self, name: str) -> None:
        """Called if the server is already stopped."""
        self.args = (
            f"The {repr(name)} server is stopped as it is."
        )

# ! CLI Exception
class IncorrectConnectionDataError(Exception):
    """Indicates incorrect data to connect to the server."""
    def __init__(self, connect_data: str) -> None:
        """Called if the connection data is incorrect."""
        self.args = (
            f"The data to connect to the server is not correct ({connect_data})."
        )