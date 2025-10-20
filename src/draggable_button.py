from dataclasses import dataclass
from textual.widgets import Button
from draggable_widget import DraggableWidget
from properties_widget import PropertiesWidget
import os


@dataclass
class ButtonProperties:
    type: str = "Button"
    name: str = "_"
    label: str = "New Button"
    command: str = "env"
    target: str = ""
    row: int = 0
    col: int = 0
    width: int = 20
    height: int = 3

class DraggableButton(DraggableWidget, PropertiesWidget, Button):    
    def __init__(self, props: ButtonProperties = None, *args, **kwargs):
        if props is None:
            props = ButtonProperties()
        Button.__init__(self, classes="draggable-button", *args, **kwargs)
        PropertiesWidget.__init__(self, props)
        DraggableWidget.__init__(self)
        self.update()
    
    def _escape_value(self, value: str) -> str:
        """Escape double quotes and backslashes in the value for safe shell usage"""
        result = value.replace('\\', '\\\\')
        result = result.replace('"', '\\"')
        result = result.replace('\'', '\\\'')
        return result
    
    def _write_shell_script(self) -> None:
        with open('a.sh', 'w') as f:
            for w in self.app.panel.get_all_widgets():
                if w.props.name and hasattr(w.props, 'value') and w.props.name[0] != '_':
                    name = w.props.name
                    value = w.props.value
                    if w.parent.name != "Main Container":
                        name = f"{w.parent.props.name}_{name}"
                    f.write(f'export {name}="{self._escape_value(value)}"\n')
            f.write(f'{self.props.command}\n')
    
    def _exec_shell_script(self) -> None:
        os.system(f"source a.sh 2>&1 > a.out")
        with open('a.out', 'r') as f:
            output = f.read()
            widget = self.app.panel.find_widget(self.props.target)
            if widget:
                widget.props.value = output
                widget.update()
            else:
                self.app.notify(f"Widget '{self.props.target}' not found", severity="error")
                # self.app.notify(f"Command Output:\n{output}", severity="information")

    def on_click(self, event: "Click") -> None:
        if event.button == 3:
            event.prevent_default()
            return

        if self.props.command:
            self._write_shell_script()
            self._exec_shell_script()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        pass
