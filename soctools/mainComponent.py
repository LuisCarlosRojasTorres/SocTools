import argparse

from .config import load_component_config
from .displayComponent import DisplayComponent
from .serverComponent import ServerComponent


class MainComponent:
    def __init__(self, config=None, display_component=None, server_component=None):
        self.config = config or load_component_config("main.ini")
        self.display_component = display_component or DisplayComponent()
        self.server_component = server_component or ServerComponent()
        self.message = self.config.get("main", "message", fallback="SocTools ready")
        self.autostart_server = self.config.getboolean(
            "main", "autostart_server", fallback=False
        )

    def status(self):
        return {
            "message": self.message,
            "display_preview": self.display_component.render(self.message),
            "server_url": self.server_component.build_url(),
        }

    def start(self):
        status = self.status()
        print(f"Display ({self.display_component.device_name}):")
        print(status["display_preview"])
        print(f"Server UI: {status['server_url']}")

        return status


def main(argv=None):
    parser = argparse.ArgumentParser(description="Start the SocTools application.")
    parser.add_argument("--message", help="Override the message shown by the components.")
    parser.add_argument(
        "--serve",
        action="store_true",
        help="Start the localhost server after showing the display preview.",
    )
    args = parser.parse_args(argv)

    component = MainComponent()

    if args.message:
        component.message = args.message

    should_serve = args.serve or component.autostart_server

    status = component.start()

    if should_serve:
        component.server_component.serve(component.message)

    return status
