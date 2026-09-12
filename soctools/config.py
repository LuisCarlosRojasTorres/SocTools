from configparser import ConfigParser
from pathlib import Path


CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"


def load_component_config(file_name: str) -> ConfigParser:
    config_path = CONFIG_DIR / file_name
    parser = ConfigParser()

    try:
        with config_path.open(encoding="utf-8") as config_file:
            parser.read_file(config_file)
    except FileNotFoundError as error:
        raise FileNotFoundError(f"Missing config file: {config_path}") from error

    return parser
