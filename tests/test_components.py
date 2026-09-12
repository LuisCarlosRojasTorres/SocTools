import unittest

from soctools.displayComponent import DisplayComponent
from soctools.mainComponent import MainComponent
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


if __name__ == "__main__":
    unittest.main()
