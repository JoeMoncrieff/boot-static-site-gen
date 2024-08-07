import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

        node  = TextNode("aa","italic","smells")
        node2 = TextNode("aa","italic","smells")
        self.assertEqual(node,node2)

        node  = TextNode("bb","italic")
        node2 = TextNode("bb","italic","smells")
        self.assertNotEqual(node, node2)

        node  = TextNode("bb","bold")
        node2 = TextNode("bb","italic")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
