import unittest
from websitegeneration import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extracttitle(self):
        markdown = "# This is my h1 heading\n" \
        "## This is a subheading that shouldn't be returned\n" \
        "...are you smoking yet?"
        result = extract_title(markdown)
        self.assertEqual(result, "This is my h1 heading")

    def test_extracttitle_notitle(self):
        markdown = "## wait you need to have a h1 heading!!!\n" \
        "cope."
        with self.assertRaises(Exception):
            result = extract_title(markdown)

    def test_extracttitle_buried(self):
        markdown = "have you had enough?\n" \
        "do you want it bad enough?\n" \
        "does it mean something to you?\n" \
        "# There's nothing we can do          "
        result = extract_title(markdown)
        self.assertEqual(result, "There's nothing we can do")