from .functions import checking_environment
from .units import (
    __name__, __version__, __author__, __email__, __url__,
    SUPPORT_PLATFORMS, CONFIG_DIRPATH, CONFIG_PATH
)
from .msm import MSManager
from .config import MSManagerConfig
from .cli import run