from io import BytesIO
import unittest
from unittest.mock import Mock, patch

from soctools.displayComponent import DisplayComponent
from soctools.mainComponent import MainComponent, run
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

    def test_display_component_preserves_existing_line_breaks(self):
        component = DisplayComponent()

        rendered = component.render("Line one\nLine two")

        self.assertEqual(rendered.splitlines()[:2], ["Line one      ", "Line two      "])

    def test_server_component_builds_html_page(self):
        component = ServerComponent()

        page = component.build_page("Status: <ok>")

        self.assertIn("SocTools Local UI", page)
        self.assertIn("Status: &lt;ok&gt;", page)

    def test_main_starts_server_once_when_requested_by_cli_or_config(self):
        mock_component = Mock()
        mock_component.autostart_server = True
        mock_component.message = "SocTools ready"
        mock_component.start.side_effect = lambda: {
            "message": mock_component.message,
            "display_preview": mock_component.message,
            "server_url": "http://127.0.0.1:8000",
        }

        with patch("soctools.mainComponent.MainComponent", return_value=mock_component):
            run(["--serve"])

        mock_component.start.assert_called_once_with()
        mock_component.server_component.serve.assert_called_once_with("SocTools ready")

    def test_main_starts_server_when_enabled_by_config_only(self):
        mock_component = Mock()
        mock_component.autostart_server = True
        mock_component.message = "SocTools ready"
        mock_component.start.side_effect = lambda: {
            "message": mock_component.message,
            "display_preview": mock_component.message,
            "server_url": "http://127.0.0.1:8000",
        }

        with patch("soctools.mainComponent.MainComponent", return_value=mock_component):
            run([])

        mock_component.start.assert_called_once_with()
        mock_component.server_component.serve.assert_called_once_with("SocTools ready")

    def test_main_uses_cli_message_override_for_server(self):
        mock_component = Mock()
        mock_component.autostart_server = True
        mock_component.message = "SocTools ready"
        mock_component.start.side_effect = lambda: {
            "message": mock_component.message,
            "display_preview": mock_component.message,
            "server_url": "http://127.0.0.1:8000",
        }

        with patch("soctools.mainComponent.MainComponent", return_value=mock_component):
            run(["--message", "Updated status"])

        self.assertEqual(mock_component.message, "Updated status")
        mock_component.start.assert_called_once_with()
        mock_component.server_component.serve.assert_called_once_with("Updated status")

    def test_server_component_serve_uses_configured_host_port_and_message(self):
        component = ServerComponent()
        component.create_handler = Mock(return_value="handler")

        with patch("soctools.serverComponent.HTTPServer") as mock_http_server:
            server_instance = mock_http_server.return_value.__enter__.return_value

            component.serve("Status ready")

        component.create_handler.assert_called_once_with("Status ready")
        mock_http_server.assert_called_once_with(
            (component.host, component.port), "handler"
        )
        server_instance.serve_forever.assert_called_once_with()

    def test_server_component_handler_writes_expected_http_response(self):
        component = ServerComponent()
        handler_class = component.create_handler("Status ready")
        handler = handler_class.__new__(handler_class)
        handler.send_response = Mock()
        handler.send_header = Mock()
        handler.end_headers = Mock()
        handler.wfile = BytesIO()

        handler.do_GET()

        expected_body = component.build_page("Status ready").encode("utf-8")
        handler.send_response.assert_called_once_with(200)
        handler.send_header.assert_any_call("Content-Type", "text/html; charset=utf-8")
        handler.send_header.assert_any_call("Content-Length", str(len(expected_body)))
        handler.end_headers.assert_called_once_with()
        self.assertEqual(handler.wfile.getvalue(), expected_body)


if __name__ == "__main__":
    unittest.main()
