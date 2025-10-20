from cProfile import label
from dataclasses import dataclass
import os
from textual.widgets import Tree
from mixins.draggable_widget import DraggableWidget
from mixins.properties_widget import PropertiesWidget
from mixins.filebacked_widget import FilebackedWidget
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
    backing_file: str = ""

class DraggableTree(DraggableWidget, PropertiesWidget, FilebackedWidget, Tree):    
    def __init__(self, props: TreeProperties = None,*args, **kwargs):
        if props is None:
            props = TreeProperties()
        Tree.__init__(self, "Root", classes="draggable-tree", *args, **kwargs)
        PropertiesWidget.__init__(self, props)
        DraggableWidget.__init__(self)
        # self.update()
        self.last_load_time = 0
        self.last_value = ""
        root_node = self.root
        child1 = root_node.add("Child 1")
        subchild = child1.add("Subchild 1.1")

    def _expand_all_nodes(self, node):
        node.expand()
        for child in node.children:
            self._expand_all_nodes(child)

    def expand_all(self):
        self._expand_all_nodes(self.root)

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
        self.backingfile_update()
        if self.last_value == self.props.value:
            return
        self.last_value = self.props.value
        try:
            data = json.loads(self.props.value)
            self.clear()
            self.add_dict_to_tree(self.root, data)
            self.expand_all()
        except json.JSONDecodeError:
            self.app.log("Invalid JSON data for Tree widget")
            pass

