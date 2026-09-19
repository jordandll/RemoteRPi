# PumpkinPi

PumpkinPi is a small Python package for controlling a PumpkinPi GPIO board and its connected LEDs/eyes through simple command-driven scripts. It includes a CLI wrapper, a socket-based server/client pattern, and a built-in animation script for demonstration and testing.

## What is included

This package contains the following modules:

- `server.py` — listens for client commands and toggles the PumpkinPi outputs.
- `client.py` — sends a command string to the server over a socket.
- `cycle.py` — runs a short cycle animation across the PumpkinPi sides and eyes.
- `cli.py` — exposes package scripts as CLI subcommands.
- `__main__.py` — package entry point for running the CLI.
- `motion-sensor.py` — motion-sensor-related logic for GPIO interaction.

## Installation

From the project root, install the package in editable mode if you are working in this repository:

```bash
pip install -e .
```

Once installed, the package exposes a `pumpkinpi` command.

## CLI usage

```bash
pumpkinpi --help
```

This will list the available subcommands, which correspond to the Python scripts in this package.

Example:

```bash
pumpkinpi server --host 127.0.0.1 --port 9001
pumpkinpi client --host 127.0.0.1 --port 9001 blink
pumpkinpi cycle
```

The CLI runs the matching script with Python automatically, so each file acts like a command.

## Example server/client flow

Start the server:

```bash
python server.py --host 127.0.0.1 --port 9001
```

Then send a command from another terminal:

```bash
python client.py --host 127.0.0.1 --port 9001 blink
```

Common command strings include:

- `blink`
- `cycle`
- `sides.left.0`
- `sides.right.4`
- `eyes.left`
- `eyes.right`

These commands are sent as UTF-8 text over a socket and interpreted by the server logic.

## Mock testing

The project supports GPIO Zero mock mode for local testing without a physical Raspberry Pi:

```bash
GPIOZERO_PIN_FACTORY=mock python server.py
```

This lets the scripts run in a simulated hardware environment while printing the actions that would have been triggered.

## Notes

This package is intended for Raspberry Pi experimentation and simple hardware control workflows. It is best used with a PumpkinPi board or a GPIO Zero mock factory during development or testing.
