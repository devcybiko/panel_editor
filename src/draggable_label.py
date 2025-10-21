from dataclasses import dataclass
from textual.widgets import Label
from mixins.draggable_widget import DraggableWidget
from mixins.properties_widget import PropertiesWidget
import os


@dataclass
class LabelProperties:
    type: str = "Label"
    name: str = "_label"
    label: str = "New Label"
    row: int = 0
    col: int = 0
    width: int = 20
    height: int = 1

class DraggableLabel(DraggableWidget, PropertiesWidget, Label):    
    def __init__(self, props: LabelProperties = None, *args, **kwargs):
        if props is None:
            props = LabelProperties()
        self.is_sizable = False
        Label.__init__(self, classes="draggable-label", *args, **kwargs)
        PropertiesWidget.__init__(self, props)
        DraggableWidget.__init__(self)
        self.update()

    def update(self, props=None):
        if props: super().update(props)
        self.props.width = len(self.props.label) or 3
        super().update()
        self.content = self.props.label
