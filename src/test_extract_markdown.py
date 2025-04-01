import unittest

from extract_markdown import extract_title


class testExtractMarkdown(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Hello, world!\n"
        self.assertEqual(
            extract_title(markdown),
            "Hello, world!",
        )

        markdown = "# Hello, world!\n\nThis is a test"
        self.assertEqual(
            extract_title(markdown),
            "Hello, world!",
        )

        markdown = "Hello, world!\n"
        with self.assertRaises(Exception):
            extract_title(markdown)

        markdown = "# Hello, world!\n# Another Title"
        self.assertEqual(
            extract_title(markdown),
            "Hello, world!",
        )
