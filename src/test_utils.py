import unittest
from html_node import HTMLNode, LeafNode, ParentNode
from textnode import TextNode
from utils import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, \
    extract_markdown_links, split_nodes_link, split_nodes_image, text_to_textnodes

class TestUtils(unittest.TestCase):

    def test_text_node_to_html_node(self):
        
        text_node1 = TextNode(text="whoa", text_type="bold")
        text_node2 = TextNode(text="whoa", text_type="italic")

        self.assertEqual(text_node_to_html_node(text_node1).to_html(), f"<b>whoa</b>")
        self.assertEqual(text_node_to_html_node(text_node2).to_html(), f"<i>whoa</i>")


        text_node3 = TextNode(text="n/a", text_type="groglir")

        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(text_node3)

        self.assertEqual(str(context.exception), "text_node.text_type does not match the accepted types")


        text_node4 = TextNode(text="whoa", text_type="image",url="example.com/pic.png")

        self.assertEqual(text_node_to_html_node(text_node4).to_html(),f"<img src=\"example.com/pic.png\" alt=\"whoa\"></img>")

        text_node5 = TextNode(text="whoa", text_type="link",url="example.com")

        self.assertEqual(text_node_to_html_node(text_node5).to_html(),f"<a href=\"example.com\">whoa</a>")
    
    
    def test_split_nodes_delimeter(self):

        node1 = TextNode("This is text with a `code block` word", "text")
        new_nodes1 = split_nodes_delimiter([node1], "`", "code")

        expected1 = \
        [ 
            TextNode("This is text with a ", "text"),
            TextNode("code block", "code"),
            TextNode(" word", "text"),
        ]

        self.assertEqual(new_nodes1,expected1)

        node2 = TextNode("This is text with two `code block` words. Here's the `second`", "text")
        new_nodes2 = split_nodes_delimiter([node2], "`", "code")

        expected2 = \
        [ 
            TextNode("This is text with two ", "text"),
            TextNode("code block", "code"),
            TextNode(" words. Here's the ", "text"),
            TextNode("second","code"),
        ]

        self.assertEqual(new_nodes2,expected2)


        node3 = TextNode("This is text with no code block words.", "text")
        new_nodes3 = split_nodes_delimiter([node3], "`", "code")

        expected3 = \
        [ 
            TextNode("This is text with no code block words.", "text")
        ]

        self.assertEqual(new_nodes3,expected3)

        node4 = TextNode("This is text with `errors.", "text")

        with self.assertRaises(ValueError) as context:
            new_nodes4 = split_nodes_delimiter([node4], "`", "code")
        
        self.assertEqual(str(context.exception), "odd number of delimeters detected")

    def test_extract_markdown(self):
        
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')])

        text2 = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text2), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
        
        self.assertEqual(extract_markdown_images(text2),[])
        self.assertEqual(extract_markdown_links(text), [])

    def test_split_nodes(self):

        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            "text",
        )
        new_nodes = split_nodes_link([node])
        compare = [
            TextNode("This is text with a link ", "text"),
            TextNode("to boot dev", "link", "https://www.boot.dev"),
            TextNode(" and ", "text"),
            TextNode(
                "to youtube", "link", "https://www.youtube.com/@bootdotdev"
            )]

        self.assertEqual(compare,new_nodes)


        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            "text",
        )
        new_nodes = split_nodes_image([node])
        compare = [
            TextNode("This is text with a link ", "text"),
            TextNode("to boot dev", "image", "https://www.boot.dev"),
            TextNode(" and ", "text"),
            TextNode(
                "to youtube", "image", "https://www.youtube.com/@bootdotdev"
            )]

        self.assertEqual(compare,new_nodes)


        no_nodes = node = TextNode(
            "This is text with no links",
            "text",
        )
        self.assertEqual(split_nodes_image([no_nodes]),[no_nodes])
        self.assertEqual(split_nodes_link([no_nodes]),[no_nodes])

    def test_text_to_textnodes(self):
            lst = text_to_textnodes("This is **text** with an *italic* word and a `code block` "+
                                    "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a "+
                                    "[link](https://boot.dev)")
            
            compare = [
                TextNode("This is ", "text"),
                TextNode("text", "bold"),
                TextNode(" with an ", "text"),
                TextNode("italic", "italic"),
                TextNode(" word and a ", "text"),
                TextNode("code block", "code"),
                TextNode(" and an ", "text"),
                TextNode("obi wan image", "image", "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", "text"),
                TextNode("link", "link", "https://boot.dev"),
            ]
            self.assertEqual(lst,compare)

            self.assertEqual(text_to_textnodes(""),[])

            with self.assertRaises(ValueError) as context:
                lst2 = text_to_textnodes("this **will throw an *error** despite being nested")

            self.assertEqual(str(context.exception),"odd number of delimeters detected")

if __name__ == "__main__":
    unittest.main()
