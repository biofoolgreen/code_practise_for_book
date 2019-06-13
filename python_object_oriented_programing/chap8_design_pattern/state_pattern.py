'''
@Description: python面向对象编程-chap8-设计模式
@Version: 
@Author: liguoying
@Date: 2019-06-11 15:01:38
'''
##################################
####          状态模式         ####
##################################

class Node:
    def __init__(self, tag_name, parent=None):
        self.parent = parent
        self.tag_name = tag_name
        self.children = []
        self.text = ""

    def __str__(self):
        if self.text:
            return self.tag_name + ": " + self.text
        return self.tag_name

## 5种节点状态：FirstTag, ChildNode, OpenTag, CloseTag, Text
## 状态转移关系： FirstTag --> ChildNode
##               ChildNode --> OpenTag
##               ChildNode --> Text
##               ChildNode --> CloseTag
##               OpenTag --> ChildNode
##               CloseTag --> ChildNode
##               Text --> ChildNode

class Parser:
    def __init__(self, parse_string):
        self.parse_string = parse_string
        self.root = None
        self.current_node = None
        self.state = FirstTag()
    
    def process(self, remaining_string):
        remaining = self.state.process(remaining_string, self)
        if remaining:
            self.process(remaining)
    
    def start(self):
        self.process(self.parse_string)


class FirstTag:
    def process(self, remaining_string, parser):
        i_start_tag = remaining_string.find("<")
        i_end_tag = remaining_string.find(">")
        tag_name = remaining_string[i_start_tag+1: i_end_tag]

        root = Node(tag_name)
        parser.root = parser.current_node = root
        parser.state = ChildNode()
        return remaining_string[i_end_tag+1: ]


class ChildNode:
    def process(self, remaining_string, parser):
        stripped = remaining_string.strip()
        if stripped.startswith("</"):
            parser.state = CloseTag()
        elif stripped.startswith("<"):
            parser.state = OpenTag()
        else:
            parser.state = TextNode()
        return stripped



class OpenTag:
    def process(self, remaining_string, parser):
        i_start_tag = remaining_string.find("<")
        i_end_tag = remaining_string.find(">")
        tag_name = remaining_string[i_start_tag+1: i_end_tag]

        node = Node(tag_name, parser.current_node)
        parser.current_node.children.append(node)
        parser.current_node = node
        parser.state = ChildNode()
        return remaining_string[i_end_tag+1:]


class CloseTag:
    def process(self, remaining_string, parser):
        i_start_tag = remaining_string.find("<")
        i_end_tag = remaining_string.find(">")
        assert remaining_string[i_start_tag + 1] == "/"
        tag_name = remaining_string[i_start_tag+2: i_end_tag]
        assert tag_name == parser.current_node.tag_name
        parser.current_node = parser.current_node.parent
        parser.state = ChildNode()
        return remaining_string[i_end_tag+1:].strip()


class TextNode:
    def process(self, remaining_string, parser):
        i_start_tag = remaining_string.find("<")
        text = remaining_string[:i_start_tag]
        parser.current_node.text = text
        parser.state = ChildNode()
        return remaining_string[i_start_tag:]

if __name__ == "__main__":

    contents = """
    <book>
        <author>Dusty Phillips</author>
        <publisher>Packt Publishing</publisher>
        <title>Python 3 Object Oriented Programming</title>
        <content>
            <chapter>
                <number>1</number>
                <title>Object Oriented Design</title>
            </chapter>
            <chapter>
                <number>2</number>
                <title>Objects In Python</title>
            </chapter>
        </content>
</book>
    """
    p = Parser(contents)
    p.start()
    nodes = [p.root]
    while nodes:
        node = nodes.pop(0)
        print(node)
        nodes = node.children + nodes
        