import unittest

from html_node import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        rep1 = HTMLNode()
        self.assertEqual("HTMLNode(None,None,None,None)",rep1.__repr__())

        rep2 = HTMLNode("a","b","c",{"d":"e"})
        self.assertEqual("HTMLNode(a,b,c,{'d': 'e'})",rep2.__repr__())
    
    def test_props_to_html(self):
        rep1 = HTMLNode(props = {"a":"1"})
        self.assertEqual(rep1.props_to_html(),"a=\"1\"")

        rep2 = HTMLNode(props = {"a":"1","b":"2"})
        self.assertEqual(rep2.props_to_html(),"a=\"1\" b=\"2\"")

    # Leaf Node Tests
    def test_leaf_to_html(self):
        l1 = LeafNode("p", "This is a paragraph of text.")
        l2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertEqual(l1.to_html(),"<p>This is a paragraph of text.</p>")
        self.assertEqual(l2.to_html(),"<a href=\"https://www.google.com\">Click me!</a>")
    
    # Parent Node Tests
    def test_parent_to_html(self):
        p1 = ParentNode(
            "p",
            [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
            ]
        )
        
        self.assertEqual("<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",p1.to_html())
        
        with self.assertRaises(ValueError):
            ParentNode("p", None).to_html()
        
        with self.assertRaises(ValueError):
            ParentNode(None,[LeafNode("b", "Bold text")]).to_html()
        
        p2 = ParentNode(
            "p",
            [
            LeafNode("b", "Bold text",props={"href":"banter.io"}),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text",props={"test":"twelve"}),
            LeafNode(None, "Normal text"),
            ]
        )

        self.assertEqual("<p><b href=\"banter.io\">Bold text</b>Normal text<i test=\"twelve\">italic text</i>Normal text</p>",p2.to_html())



if __name__ == "__main__":
    unittest.main()
