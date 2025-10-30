
from cProfile import label
from dataclasses import dataclass
import os
import json
import pyperclip
from textual.widgets import Tree
from mixins.draggable_widget import DraggableWidget
from mixins.properties_widget import PropertiesWidget
from mixins.filebacked_widget import FilebackedWidget



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
    key: str = ""
    target: str = ""

class DraggableTree(DraggableWidget, PropertiesWidget, FilebackedWidget, Tree):    
    def __init__(self, props: TreeProperties = None,*args, **kwargs):
        if props is None:
            props = TreeProperties()
        Tree.__init__(self, "<empty>", classes="draggable-tree", *args, **kwargs)
        PropertiesWidget.__init__(self, props)
        DraggableWidget.__init__(self)
        FilebackedWidget.__init__(self)
        self.update()
        self.last_load_time = 0
        self.last_value = ""

    def _expand_all_nodes(self, node):
        node.expand()
        for child in node.children:
            self._expand_all_nodes(child)

    def expand_all(self):
        self._expand_all_nodes(self.root)

    def _add_list_to_tree(self, node, data):
        key_name = self.props.key
        for index, element in enumerate(data):
            if type(element) not in [dict, list]:
                child = node.add_leaf(child_name)
            else:
                child_name = "child:" + element.get(key_name, f"child: {index}")
                child = node.add(child_name)
                self.add_json_to_tree(child, element)

    def _add_dict_to_tree(self, node, obj):
        for key, value in obj.items():
            if type(value) not in [dict, list]:
                child = node.add_leaf(f"{key}: {value}")
            else:
                child = node.add(f"{key}")
                self.add_json_to_tree(child, data=value)

    def add_json_to_tree(self, node, data):
        if isinstance(data, dict):
            self._add_dict_to_tree(node, data)
        elif isinstance(data, list):
            self._add_list_to_tree(node, data)
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
            root_name = self.props.backing_file or self.props.label or "Root"
            self.root.label = root_name
            self.add_json_to_tree(self.root, data)
            self.expand_all()
        except json.JSONDecodeError:
            self.app.log("Invalid JSON data for Tree widget")
            pass

    def on_click(self, event):
        # Try to get the node from the event if possible
        node = getattr(event, "node", None)
        if node is None:
            # Fallback: try to get the highlighted node
            node = self.cursor_node if hasattr(self, "cursor_node") else None
        if node:
            text = str(node.label).split(":",1)[1] if ":" in str(node.label) else str(node.label)
            text = text.strip()
            pyperclip.copy(text)
            if self.props.target:
                widget = self.app.panel.find_widget(self.props.target)
                if widget and hasattr(widget.props, 'value'):
                    widget.props.value = text
                    widget.update()
                else:
                    self.app.notify(f"Widget '{self.props.target}' not found", severity="error")
