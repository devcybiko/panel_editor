from dataclasses import dataclass
import os
from textual.widgets import TextArea
from mixins.draggable_widget import DraggableWidget
from mixins.properties_widget import PropertiesWidget
from mixins.filebacked_widget import FilebackedWidget

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
    backing_file: str = ""
    readonly: bool = False

class DraggableTextArea(DraggableWidget, PropertiesWidget, FilebackedWidget, TextArea):    
    def __init__(self, props: TextAreaProperties = None, *args, **kwargs):
        if props is None:
            props = TextAreaProperties()
        TextArea.__init__(self, classes="draggable-textarea", show_line_numbers=False, *args, **kwargs)
        PropertiesWidget.__init__(self, props)
        DraggableWidget.__init__(self)
        FilebackedWidget.__init__(self)
        self.update()
    
    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        """Handle when the textarea content changes"""
        self.props.value = self.text
    
    def update(self, props=None):
        super().update(props)
        self.border_title = self.props.name
        self.backingfile_update()
        if self.last_value == self.props.value:
            return
        self.last_value = self.props.value
        self.text = self.props.value

    def scroll_to(self, pattern):
        """Scroll the given TextArea to the first occurrence of pattern and position the cursor there"""
        content = self.text
        index = content.find(pattern)
        if index != -1:
            self.cursor_position = index
            self.focus()         # Ensure the widget is focused
            self.refresh()       # Force redraw
        return index