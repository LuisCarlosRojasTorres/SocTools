from textwrap import wrap

from .config import load_component_config


class DisplayComponent:
    def __init__(self, config=None):
        self.config = config or load_component_config("displayComponent.ini")
        self.device_name = self.config.get("display", "device_name", fallback="Nokia 5110")
        self.columns = self.config.getint("display", "columns", fallback=14)
        self.rows = self.config.getint("display", "rows", fallback=6)

    def render(self, message: str) -> str:
        wrapped_lines = wrap(message, self.columns) or [""]
        visible_lines = wrapped_lines[: self.rows]
        return "\n".join(line.ljust(self.columns) for line in visible_lines)

