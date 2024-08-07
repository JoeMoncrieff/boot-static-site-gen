import re
from html_node import HTMLNode, LeafNode, ParentNode
from utils import text_to_textnodes, text_node_to_html_node

def markdown_to_blocks(markdown):
    output = []
    for block in re.findall(r"(.+((\n).+)*)",markdown):      
        output.append(block[0])
    return(output)

def b_t_b_t_helper(markdown):
    count = 0
    if markdown == "":
        return False
    
    lines = markdown.split("\n")
    for i in range(0,len(lines)):
        if lines[i][0:3] != f"{i+1}. ":
            return False
        
    return True

def block_to_block_type(markdown):
    """ Headings start with 1-6 # characters, followed by a space and then the heading text."""
    if re.match(r"(?<!#)##?#?#?#?#?(?!#) .+",markdown):
        return "heading"
    
    elif re.match(r"```[\s\S]*```",markdown):
        return "code"
        """ Code blocks must start with 3 backticks and end with 3 backticks. """
    elif re.match(r">.*(\n>.*)*", markdown):
        """ Every line in a quote block must start with a > character. """
        return "quote"
    elif re.match(r"[\*-] .*(\n>.*)*",markdown):
        """ Every line in an unordered list block must start with a * or - character, 
        followed by a space. """
        return "unordered_list"
    elif b_t_b_t_helper(markdown):
        """ Every line in an ordered list block must start with a number followed by a . character and a space. 
        The number must start at 1 and increment by 1 for each line. """
        return "ordered_list"
    else:
        """ If none of the above conditions are met, the block is a normal paragraph."""
        return "paragraph"
        
def markdown_to_html_node(markdown):
    # Split the markdown into blocks (you already have a function for this)
    big_children = []
    blocks = markdown_to_blocks(markdown)
    # Loop over each block:
    for block in blocks:
        block_type = block_to_block_type(block)
        node = None
        match block_type:
            case "paragraph":
                children = list(map(text_node_to_html_node, text_to_textnodes(block)))
                node = ParentNode(tag="p", children=children)
                big_children.append(node)
            
            case "code":
                #take away the back ticks
                children = list(map(text_node_to_html_node, text_to_textnodes(block[3:-3])))
                node = ParentNode(tag="code", children=children)
                node = ParentNode(tag="pre", children=[node])
                big_children.append(node)
            
            case "heading":
                # take away the heading thing
                b = block.lstrip("#").lstrip()

                number = len(block) - len(b) - 1

                children = list(map(text_node_to_html_node, text_to_textnodes(b)))
                node = ParentNode(tag=f"h{number}", children=children)
                big_children.append(node)

            case "quote":
                #take away quote pointer from each line
                block = "\n".join(x[1:] for x in block.split("\n"))
                children = list(map(text_node_to_html_node, text_to_textnodes(block)))
                node = ParentNode(tag="blockquote", children=children)
                big_children.append(node)

            case "ordered_list":
                block_break = block.split("\n")
                for i in range(0,len(block_break)):
                    #need to give each line an <li> tag
                    block_break[i] = block_break[i][3:]
                    babies = list(map(text_node_to_html_node, text_to_textnodes(block_break[i])))
                    block_break[i] = ParentNode(tag="li",children=babies)
                node = ParentNode(tag="ol",children=block_break)
                big_children.append(node)
                
            case "unordered_list":
                block_break = block.split("\n")
                for i in range(0,len(block_break)):
                    #need to give each line an <li> tag
                    block_break[i] = block_break[i][2:]
                    babies = list(map(text_node_to_html_node, text_to_textnodes(block_break[i])))
                    block_break[i] = ParentNode(tag="li",children=babies)
                node = ParentNode(tag="ul",children=block_break)
                big_children.append(node)

            case _:
                raise ValueError("not one of the designated block types")
    return ParentNode(tag="div", children=big_children)