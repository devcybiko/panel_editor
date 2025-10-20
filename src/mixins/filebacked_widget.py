from dataclasses import dataclass
import os
from textual.events import MouseDown, MouseUp, MouseMove
from properties_sheet import PropertiesSheet
from widget_factory import WidgetFactory

class FilebackedWidget:
    def __init__(self):
        self.last_value = ""
        self.last_load_time = 0

    def backingfile_update(self) -> None:
        if not self.props.backing_file:
            return None
        try:
            file_mod_time = os.path.getmtime(self.props.backing_file)
            if file_mod_time > self.last_load_time:
                self.last_load_time = file_mod_time
                with open(self.props.backing_file, "r", encoding="utf-8") as f:
                        self.props.value = f.read()
        except Exception as e:
            self.props.value = f"{self.props.type}: ERROR reading file {self.props.backing_file}: {e}"
