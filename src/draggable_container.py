from dataclasses import dataclass
from textual.containers import Container
from mixins.draggable_widget import DraggableWidget
from mixins.properties_widget import PropertiesWidget


@dataclass
class ContainerProperties:
    type: str = "Container"
    name: str = "New Container"
    label: str = "New Container"
    row: int = 0
    col: int = 0
    width: int = 30
    height: int = 15

class DraggableContainer(DraggableWidget, PropertiesWidget, Container):    
    def __init__(self, props: ContainerProperties = None, *args, **kwargs):
        if props is None:
            props = ContainerProperties()
        self.type = "Container"
        Container.__init__(self, classes="draggable-container", *args, **kwargs)
        PropertiesWidget.__init__(self, props)
        DraggableWidget.__init__(self)

        self.update()
        
    def update(self, props=None):
        super().update(props)
        self.border_title = self.props.label
    