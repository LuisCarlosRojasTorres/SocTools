import unittest
from unittest.mock import Mock, patch

from soctools.displayComponent import DisplayComponent
from soctools.mainComponent import MainComponent, main
from soctools.serverComponent import ServerComponent


class SocToolsComponentTests(unittest.TestCase):
    def test_main_component_loads_root_configs(self):
        component = MainComponent()

        status = component.status()

        self.assertEqual(status["message"], "SocTools ready")
        self.assertEqual(status["server_url"], "http://127.0.0.1:8000")
        self.assertIn("SocTools ready", status["display_preview"])

    def test_display_component_respects_configured_rows(self):
        component = DisplayComponent()

        rendered = component.render("One two three four five six seven eight nine")

        self.assertLessEqual(len(rendered.splitlines()), component.rows)

    def test_server_component_builds_html_page(self):
        component = ServerComponent()

        page = component.build_page("Status: <ok>")

        self.assertIn("SocTools Local UI", page)
        self.assertIn("Status: &lt;ok&gt;", page)

    def test_main_starts_server_once_when_requested_by_cli_or_config(self):
        mock_component = Mock()
        mock_component.autostart_server = True
        mock_component.message = "SocTools ready"
        mock_component.start.return_value = {
            "message": "SocTools ready",
            "display_preview": "SocTools ready",
            "server_url": "http://127.0.0.1:8000",
        }

        with patch("soctools.mainComponent.MainComponent", return_value=mock_component):
            main(["--serve"])

        mock_component.start.assert_called_once_with()
        mock_component.server_component.serve.assert_called_once_with("SocTools ready")

    def test_main_starts_server_when_enabled_by_config_only(self):
        mock_component = Mock()
        mock_component.autostart_server = True
        mock_component.message = "SocTools ready"
        mock_component.start.return_value = {
            "message": "SocTools ready",
            "display_preview": "SocTools ready",
            "server_url": "http://127.0.0.1:8000",
        }

        with patch("soctools.mainComponent.MainComponent", return_value=mock_component):
            main([])

        mock_component.start.assert_called_once_with()
        mock_component.server_component.serve.assert_called_once_with("SocTools ready")


if __name__ == "__main__":
    unittest.main()
