import unittest
from block_utils import ( markdown_to_blocks,
                         block_to_block_type,
                          markdown_to_html_node )

class TestBlockUtils(unittest.TestCase):

    def test_markdown_to_blocks(self):
        
        txt = markdown_to_blocks("# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n\n\n\n\n\n\n\n\n" +
                   "* This is the first list item in a list block\n"+
                   "* This is a list item\n"+
                   "* This is another list item")

        self.assertEqual(txt,["# This is a heading",
                              "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                              "* This is the first list item in a list block\n"+
                              "* This is a list item\n"+
                              "* This is another list item"])

        self.assertEqual(markdown_to_blocks(""),[])

    def test_block_to_block_type(self):

        txt = markdown_to_blocks("# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n\n\n\n\n\n\n\n\n" +
                   "* This is the first list item in a list block\n"+
                   "* This is a list item\n"+
                   "* This is another list item\n\n"+
                   "```this block\nis a bunch of code\n```\n\n"+
                   "```this is just a paragraph though\n\n\n"+
                   "1. list\n2. list\n3. list\n4. list\n\n"+
                   ">quote\n>quot\n>quo\n>qu\n\n"+
                   "####### not a heading")
        
        self.assertEqual(block_to_block_type(txt[0]),"heading")
        self.assertEqual(block_to_block_type(txt[1]),"paragraph")
        self.assertEqual(block_to_block_type(txt[2]),"unordered_list")
        self.assertEqual(block_to_block_type(txt[3]),"code")
        self.assertEqual(block_to_block_type(txt[4]),"paragraph")
        self.assertEqual(block_to_block_type(txt[5]),"ordered_list")
        self.assertEqual(block_to_block_type(txt[6]),"quote")
        self.assertEqual(block_to_block_type(txt[7]),"paragraph")
    
    def test_markdown_to_html_node(self):

        txt =("# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n\n\n\n\n\n\n\n\n" +
                   "* This is the first list item in a list block\n"+
                   "* This is a list item\n"+
                   "* This is another list item\n\n"+
                   "```this block\nis a bunch of code\n```\n\n"+
                   "This is **text** with an *italic* word and a `code block` "+
                    "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a "+
                    "[link](https://boot.dev)\n\n"+
                   "1. list\n2. list\n3. list\n4. list\n\n"+
                   ">quote\n>quot\n>quo\n>qu\n\n"+
                   "####### not a heading")
        
        txt1 = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n\n\n\n\n\n\n\n\n"
        #print(markdown_to_html_node(txt).to_html())

if __name__ == "__main__":
    unittest.main()
