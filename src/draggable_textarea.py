from dataclasses import dataclass
import os
from textual.widgets import TextArea
from mixins.draggable_widget import DraggableWidget
from mixins.properties_widget import PropertiesWidget
from mixins.filebacked_widget import FilebackedWidget
import re

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

    def _find_in_rows(self, lines, row, col, pattern, regex):
        self.app.notify(f"Searching for pattern '{pattern}' at {row, col}", severity="info")
        for line in lines[row:]:
            if regex:
                match = re.search(pattern, line[col:])
                new_col = match.start() if match else -1
            else:
                new_col = line[col:].find(pattern)
            if new_col != -1:
                self.cursor_location = (row, new_col)
                self.focus()         # Ensure the widget is focused
                self.refresh()       # Force redraw
                return self.cursor_location
            col = 0
            row += 1
        return (row, col)


    def find_pattern(self, pattern, case_sensitive=True, regex=False):
        """Scroll the given TextArea to the first occurrence of pattern and position the cursor there"""
        content = self.text
        if not case_sensitive:
            content = content.lower()
            pattern = pattern.lower()
        lines = content.splitlines()
        row, col = self.cursor_location
        self.app.notify(f"cURSOR= {row, col}", severity="info")
        col += 1
        row, col = self._find_in_rows(lines, row, col, pattern, regex)
        if row < len(lines):
            self.app.notify(f"Pattern found {row, col}", severity="info")
            return (row, col)
        self.app.notify("Reached end of document, continuing search from top.", severity="info")
        row = 0
        col = 0
        row, col = self._find_in_rows(lines, row, col, pattern, regex)
        if row < len(lines):
            self.app.notify(f"^ Pattern found {row,col}", severity="info")
            return (row, col)
        self.app.notify("Pattern not found.", severity="warning")
        return (row, col)