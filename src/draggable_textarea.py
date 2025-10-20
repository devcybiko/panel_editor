from dataclasses import dataclass
from textual.widgets import TextArea
from draggable_widget import DraggableWidget
from properties_widget import PropertiesWidget

@dataclass
class TextAreaProperties:
    type: str = "TextArea"
    name: str = "_"
    value: str = ""
    row: int = 0
    col: int = 0
    width: int = 40
    height: int = 3
    placeholder: str = "placeholder"

class DraggableTextArea(DraggableWidget, PropertiesWidget, TextArea):    
    def __init__(self, props: TextAreaProperties = None, *args, **kwargs):
        if props is None:
            props = TextAreaProperties()
        TextArea.__init__(self, classes="draggable-textarea", show_line_numbers=False, *args, **kwargs)
        PropertiesWidget.__init__(self, props)
        DraggableWidget.__init__(self)
        self.update()
    
    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        """Handle when the textarea content changes"""
        self.props.value = self.text
    
    def update(self, props=None):
        super().update(props)
        self.border_title = self.props.name
        self.text = self.props.value