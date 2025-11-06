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
    placeholder: str = None
    backing_file: str = ""
    readonly: bool = False
    soft_wrap: bool = False
    language: str = None
    show_line_numbers: bool = False

class DraggableTextArea(DraggableWidget, PropertiesWidget, FilebackedWidget, TextArea):    
    def __init__(self, props: TextAreaProperties = None, *args, **kwargs):
        if props is None:
            props = TextAreaProperties()
        TextArea.__init__(self, classes="draggable-textarea", *args, **kwargs)
        PropertiesWidget.__init__(self, props)
        DraggableWidget.__init__(self)
        FilebackedWidget.__init__(self)
        # self.language = props.language
        self.update()
    
    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        """Handle when the textarea content changes"""
        self.props.value = self.text
        pass
    
    def _set_code_editor(self, props=None):
        if not props:
            props = self.props
        self.soft_wrap = props.soft_wrap
        self.tab_behavior = "indent"
        self.read_only = props.readonly
        self.show_cursor = True
        self.show_line_numbers = props.show_line_numbers
        self.disabled = False
        self.tooltip = None
        self.compact = False
        self.highlight_cursor_line = True
        self.placeholder = props.placeholder


    def update(self, props=None):
        # GLS - HACK - removing "language" support for now as it causes issues with TextArea base class
        self.props.language = None
        if props is not None:
            props["language"] = None
        super().update(props)
        if self.text != self.props.value:
            self.text = self.props.value
        self.border_title = self.props.name
        self.backingfile_update()
        # self._set_code_editor(self.props)
        pass

    def _find_in_rows(self, lines, row, col, pattern, regex):
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
        col += 1
        row, col = self._find_in_rows(lines, row, col, pattern, regex)
        if row < len(lines):
            return (row, col)
        row = 0
        col = 0
        row, col = self._find_in_rows(lines, row, col, pattern, regex)
        if row < len(lines):
            return (row, col)
        self.app.notify("Pattern not found.", severity="warning")
        return (row, col)