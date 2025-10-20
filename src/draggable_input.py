from dataclasses import dataclass
from textual.widgets import Input
from draggable_widget import DraggableWidget
from properties_widget import PropertiesWidget

@dataclass
class InputProperties:
    type: str = "Input"
    name: str = "_"
    value: str = ""
    row: int = 0
    col: int = 0
    width: int = 40
    height: int = 3
    placeholder: str = "placeholder"

class DraggableInput(DraggableWidget, PropertiesWidget, Input):    
    def __init__(self, props: InputProperties = None, *args, **kwargs):
        if props is None:
            props = InputProperties()
        Input.__init__(self, classes="draggable-input", *args, **kwargs)
        PropertiesWidget.__init__(self, props)
        DraggableWidget.__init__(self)
        self.update()
    
    def on_input_changed(self, event: Input.Changed) -> None:
        self.props.value = self.value
    
