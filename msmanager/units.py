import os
from platformdirs import user_config_dir

# ! Metadata
__prog_name__ = "msmanager"
__title__ = "MSManager (Mindustry Servers Manager)"
__version__ = "0.4.7.dev1"
__author__ = "RCR"
__email__ = "semina054@gmail.com"
__url__ = "https://github.com/RCR-OOP/msmanager"

# ! Constants
SUPPORT_PLATFORMS = [
    "windows-amd64", "windows-x86_64", "linux-x86_64"
]
CONFIG_DIRPATH      = user_config_dir(__prog_name__, __author__, ensure_exists=True)
CONFIG_PATH         = os.path.join(CONFIG_DIRPATH, "msmanager_config.json")
ERRORLOG_DIRPATH    = os.path.join(CONFIG_DIRPATH, "errors")

# ! Regex
COLOR_PATTERN = r"\x1b\[[0-9;]*m"

# ! Creating directoryes
os.makedirs(ERRORLOG_DIRPATH, exist_ok=True)