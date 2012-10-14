from core.test_utilities import get_data
from core.templatetags import text_processors

from django.test import TestCase
from django.utils import html


class TextProcessorsMarkdownWrapperTest(TestCase):

    def test_processors_wrapper(self):
        """Tests that wrapper for processor works by testing bold's syntax. Real tests for Markdown processor can be found in it's package."""
        data = get_data()
        expected = "<p><strong>{}</strong></p>\n".format(data)
        # Markdown's representation of bold text.
        actual = text_processors.markdown("**{}**".format(data))
        self.assertEqual(expected, actual)

    def test_xss_vulnerability(self):
        """Tests that processor's wrapper takes care of XSS vulnerability."""
        data = "<script>alert('{}');</script>".format(get_data())
        expected = "<p>{}</p>\n".format(html.escape(data))
        actual = text_processors.markdown(data)
        self.assertEqual(expected, actual)
