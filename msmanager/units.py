import os
from platformdirs import user_config_dir

# ! Metadata
__name__ = "msmanager"
__version__ = "0.1.0"
__author__ = "RCR"
__email__ = "semina054@gmail.com"
__url__ = "https://github.com/RCR-OOP/msmanager"

# ! Constants
SUPPORT_PLATFORMS = [
    "windows-amd64", "windows-x86_64", "linux-x86_64"
]
CONFIG_DIRPATH = user_config_dir(__name__, __author__)
CONFIG_PATH = os.path.join(CONFIG_DIRPATH, "msmanager-config.json")