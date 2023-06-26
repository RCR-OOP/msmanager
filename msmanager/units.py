import os
from platformdirs import user_config_dir

# ! Metadata
__name__ = "msmanager"
__title__ = "MSManager (Mindustry Servers Manager)"
__version__ = "0.2.2.dev1"
__author__ = "RCR"
__email__ = "semina054@gmail.com"
__url__ = "https://github.com/RCR-OOP/msmanager"

# ! Constants
SUPPORT_PLATFORMS = [
    "windows-amd64", "windows-x86_64", "linux-x86_64"
]
CONFIG_DIRPATH = user_config_dir(__name__, __author__)
CONFIG_PATH = os.path.join(CONFIG_DIRPATH, "msmanager_config.json")

# ! For Parsing
COLORS_STRINGS_REPLACEBLE = { f"\x1b[{i}m": "" for i in range(100) }
