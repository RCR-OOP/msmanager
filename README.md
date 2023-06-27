# MSManager
## Description
Manager for managing Mindustry servers.
## Install
```shell
python3 -m pip install -U msmanager
```
## Usage
```
Usage: python -m msmanager [OPTIONS] COMMAND [ARGS]...

Options:
  -nce, --not-check-environment  Disables checks for GNU Screen, Java and
                                 system support.
  -d, --debug                    Enables debug mode of operation.
  --version                      Show the version and exit.
  --help                         Show this message and exit.

Commands:
  add     Add a server to the config.
  list    List of servers in the config.
  ping    Server status check.
  remove  Remove the server from the config.
  start   Run the server.
  stop    Stop the server.
```
