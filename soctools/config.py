from configparser import ConfigParser
from pathlib import Path


CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"


def load_component_config(file_name: str) -> ConfigParser:
    config_path = CONFIG_DIR / file_name
    parser = ConfigParser()

    if not parser.read(config_path):
        raise FileNotFoundError(f"Missing config file: {config_path}")

    return parser

