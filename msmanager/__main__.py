import msmanager
from rich.console import Console

console = Console()
try:
    pass
except:
    console.print_exception(show_locals=True, word_wrap=True)