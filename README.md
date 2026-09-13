# SocTools

Python project structure for ESP32 and Raspberry Pi display support.

## Components

- `soctools/mainComponent.py`: starts the program and coordinates the other components.
- `soctools/displayComponent.py`: display UI component for physical displays such as the Nokia 5110.
- `soctools/serverComponent.py`: localhost UI component backed by a built-in HTTP server.

Each component has its own configuration file in `/config`:

- `/config/main.ini`
- `/config/displayComponent.ini`
- `/config/serverComponent.ini`

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m soctools
```

To start the localhost UI server:

```bash
python -m soctools --serve
```

## Dependencies
Some packages shall be installed this way:

```
sudo apt-get install python3-rpi.gpio
```