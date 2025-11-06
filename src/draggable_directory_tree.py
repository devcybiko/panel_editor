from dataclasses import dataclass
from textual.widgets import DirectoryTree
from mixins.draggable_widget import DraggableWidget
from mixins.properties_widget import PropertiesWidget
from mixins.filebacked_widget import FilebackedWidget
import re

@dataclass
class DirectoryTreeProperties:
    type: str = "DirectoryTree"
    name: str = "_"
    value: str = ""
    row: int = 0
    col: int = 0
    width: int = 40
    height: int = 20
    path: str = "."

class DraggableDirectoryTree(DraggableWidget, PropertiesWidget, DirectoryTree):    
    def __init__(self, props: DirectoryTreeProperties = None, *args, **kwargs):
        if props is None:
            props = DirectoryTreeProperties()
        DirectoryTree.__init__(self, path=props.path, classes="draggable-directory-tree", *args, **kwargs)
        PropertiesWidget.__init__(self, props)
        DraggableWidget.__init__(self)
        self.update()
    

    def update(self, props=None):
        super().update(props)
        self.border_title = self.props.name