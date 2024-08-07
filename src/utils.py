from textnode import TextNode
from html_node import HTMLNode, LeafNode, ParentNode

import re


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case "text":
            return LeafNode(value=text_node.text)
        case "bold":
            return LeafNode(tag = "b", value=text_node.text)
        case "italic":
            return LeafNode(tag = "i", value=text_node.text)
        case "code":
            return LeafNode(tag = "code", value=text_node.text)
        case "link":
            return LeafNode(tag = "a", value=text_node.text, props={"href":text_node.url})
        case "image":
            return LeafNode(tag = "img", value="", props={"src":text_node.url,
                                                "alt":text_node.text})
        case _:
            raise ValueError("text_node.text_type does not match the accepted types")

def split_nodes_delimiter(old_nodes,delimiter,text_type):
    output = []
    for node in old_nodes:
        curr_arr = node.text.split(delimiter)

        if len(curr_arr) == 1:
            if node.text != "":
                output.append(node)
        elif len(curr_arr) %2 == 0:
            raise ValueError("odd number of delimeters detected")
        else:
            for i in range(0,len(curr_arr)):
                if i % 2 == 0:
                    txt = curr_arr[i]
                    if txt != '':
                        output.append(TextNode(text = txt,text_type="text"))
                else:
                    output.append(TextNode(text = curr_arr[i],text_type=text_type))

    return output

def extract_markdown_images(text):
    full_expression = r"\!\[(.*?)\]\((.*?)\)"
    return(re.findall(full_expression,text))

def extract_markdown_links(text):
    full_expression = r"(?<!\!)\[(.*?)\]\((.*?)\)"
    return(re.findall(full_expression,text))

def split_nodes_image(old_nodes):
    output = []
    
    for node in old_nodes:
        basic_strings = re.split(r"!\[.*?\]\(.*?\)",node.text)
        image_strings = extract_markdown_images(node.text)
        
        if len(basic_strings) == 1:
            if node.text != "":
                output.append(node)
        else:
            b_s_count = 0
            i_s_count = 0
            for i in range(0,len(basic_strings) + len(image_strings)):
                if i % 2 == 0:
                    txt = basic_strings[b_s_count]
                    if txt != '':
                        output.append(TextNode(text = txt,text_type="text"))
                    b_s_count +=1
                else:
                    output.append(TextNode(text = image_strings[i_s_count][0],text_type="image",url=image_strings[i_s_count][1]))
                    i_s_count+=1
                
    return output

def split_nodes_link(old_nodes):
    output = []
    for node in old_nodes:
        basic_strings = re.split(r"(?<!\!)\[.*?\]\(.*?\)",node.text)
        image_strings = extract_markdown_links(node.text)

        if len(basic_strings) == 1:
            if node.text != "":
                output.append(node)
        else:
            b_s_count = 0
            i_s_count = 0
            for i in range(0,len(basic_strings) + len(image_strings)):
                if i % 2 == 0:
                    txt = basic_strings[b_s_count]
                    if txt != '':
                        output.append(TextNode(text = txt,text_type="text"))
                    b_s_count +=1
                else:
                    output.append(TextNode(text = image_strings[i_s_count][0],text_type="link",url=image_strings[i_s_count][1]))
                    i_s_count+=1
                
    return output

def text_to_textnodes(text):
    txt_node = TextNode(text,"text")
    # b, i, code, a, img
    nodes = split_nodes_image([txt_node])
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes,"**", "bold")
    nodes = split_nodes_delimiter(nodes,"*", "italic")
    nodes = split_nodes_delimiter(nodes,"`", "code")

    return nodes



