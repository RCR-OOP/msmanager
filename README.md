# MSManager
## Description
Manager for managing Mindustry servers.

## Install
```
python3 -m pip install -U msmanager
```

## Usage
```
Usage: python -m msmanager [OPTIONS] COMMAND [ARGS]...

Options:
  --check-environment       Enables checks for GNU Screen, Java and system
                            support.
  -d, --debug               Enables debug mode of operation.
  -f, --format [text|json]  The output format.  [default: text]
  --version                 Show the version and exit.
  --help                    Show this message and exit.

Commands:
  add       Add a server to the config.
  list      List of servers in the config.
  ping      Server status check.
  remove    Remove the server from the config.
  restart   Restart the server(s).
  start     Run the server(s).
  stop      Stop the server(s).
  watchdog  The active process of monitoring servers, which, if the...
```
