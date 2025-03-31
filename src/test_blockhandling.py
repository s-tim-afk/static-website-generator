import unittest
from blockhandling import markdown_to_blocks, BlockType, block_to_blocktype

class TestBlockHandling(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
                This is **bolded** paragraph

                This is another paragraph with _italic_ text and `code` here
                This is the same paragraph on a new line

                - This is a list
                - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_blocktype_getter_ulist(self):
        block = "- This is a list\n- with items"
        self.assertEqual(block_to_blocktype(block), BlockType.ULIST)

    def test_blocktype_getter_olist(self):
        block = "1. This is a list\n2. with items\n3. and even more\n4. items"
        self.assertEqual(block_to_blocktype(block), BlockType.OLIST)

    def test_blocktype_getter_paragraph(self):
        block = "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line"
        self.assertEqual(block_to_blocktype(block), BlockType.PARA)

    def test_blocktype_getter_heading(self):
        block = "# This is a heading with _italic_ text and `code`"
        self.assertEqual(block_to_blocktype(block), BlockType.HEAD)

    def test_blocktype_getter_code(self):
        block = "```This is code for a program that does horrible things```"
        self.assertEqual(block_to_blocktype(block), BlockType.CODE)

    def test_blocktype_getter_not_code(self):
        block = "```but this isn't code..."
        self.assertEqual(block_to_blocktype(block), BlockType.PARA)

    def test_blocktype_getter_quote(self):
        block = ">Hey!\n>I've been thinking of only you\n" \
        ">Hey!\n>I've never seen you _but in a dream_\n" \
        ">Hey!\n>You found your fortune in Chinatown\n" \
        ">Hey!\n>To the very last detail you're the one\n" \
        ">You're life is broken into\n>Five easy pieces\n" \
        ">But who can bring them all\n>Back again?\n" \
        ">Don't go to Houston, you should\n>Come to Tokyo\n" \
        ">Would you believe in a\n>Big chance meeting?\n" \
        ">I'm just dying\n" \
        ">I'm just dying\n" \
        ">I'm just dying to see!"
        self.assertEqual(block_to_blocktype(block), BlockType.QUOTE)

if __name__ == "__main__":
    unittest.main()