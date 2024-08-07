import functools

class HTMLNode:
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        output = ""
        if self.props == None:
            return ""
        for key,value in self.props.items():
            output+= f"{key}=\"{value}\" "
        return output[:-1]

    def __repr__(self):
        return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None,  props=None):
        super().__init__(tag=tag, value=value, props=props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError
        elif self.tag == None:
            return str(self.value)
        elif self.props != None:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
    def __init__(self,tag=None, children=None,props=None):
        super().__init__(tag=tag,children=children,props=props)
    
    def to_html(self):
        def html_helper(output_str,node):
            return output_str + node.to_html()

        if self.children == None:
            raise ValueError("no children innit")
        elif self.tag == None:
            raise ValueError("no tag innit")
        elif self.props == None:
            return f"<{self.tag}>{functools.reduce(html_helper,self.children,'')}</{self.tag}>"
        else:
            return f"<{self.tag} {self.props_to_html()}>{functools.reduce(html_helper,self.children,'')}</{self.tag}>"
