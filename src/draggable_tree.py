from cProfile import label
from dataclasses import dataclass
from textual.widgets import Tree
from draggable_widget import DraggableWidget
from properties_widget import PropertiesWidget
import json

@dataclass
class TreeProperties:
    type: str = "Tree"
    name: str = "_"
    label: str = "Root"
    value: str = ""
    row: int = 0
    col: int = 0
    width: int = 40
    height: int = 3
    placeholder: str = "placeholder"

class DraggableTree(DraggableWidget, PropertiesWidget, Tree):    
    def __init__(self, props: TreeProperties = None,*args, **kwargs):
        if props is None:
            props = TreeProperties()
        Tree.__init__(self, "Root", classes="draggable-tree", *args, **kwargs)
        PropertiesWidget.__init__(self, props)
        DraggableWidget.__init__(self)
        # self.update()
        root_node = self.root
        child1 = root_node.add("Child 1")
        subchild = child1.add("Subchild 1.1")

    def add_dict_to_tree(self, node, data):
        if isinstance(data, dict):
            for key, value in data.items():
                if type(value) in (dict, list):
                    child = node.add(str(key))
                    self.add_dict_to_tree(child, value)
                else:
                    node.add_leaf(f"{key}: {value}")
        elif isinstance(data, list):
            i = 0
            for item in data:
                child = node.add(f"Child {i}")
                self.add_dict_to_tree(child, item)
                i += 1
        else:
            node.add(str(data))
    
    def update(self, props=None):
        super().update(props)
        self.border_title = self.props.name
        if not self.props.value:
            return
        try:
            data = json.loads(self.props.value)
            self.clear()
            self.add_dict_to_tree(self.root, data)
        except json.JSONDecodeError:
            self.app.log("Invalid JSON data for Tree widget")
            pass

