from dataclasses import dataclass
import json
from munch import DefaultMunch
from textual.widgets import Button
from mixins.draggable_widget import DraggableWidget
from mixins.properties_widget import PropertiesWidget, text, code
import os


@dataclass
class ButtonProperties:
    type: str = "Button"
    name: str = "_"
    label: str = "New Button"
    python: bool = False
    command: code = "env"
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
    
    def _create_context(self) -> str:
        context = {}
        for w in self.app.panel.get_all_widgets():
            if w.props.name and hasattr(w.props, 'value') and w.props.name[0] != '_':
                name = w.props.name
                value = w.props.value
                context[name] = value
        return context

    def _python_eval(self, context: dict) -> None:
        _ = DefaultMunch.fromDict(context)
        result = None
        try:
            exec(self.props.command)
            result = _.result
        except Exception as e:
            self.app.notify(f"Error executing Python command: {e}", severity="error")
            return
        if self.props.target and result:
            if type(result) == dict:
                result = json.dumps(result)
            widget = self.app.panel.find_widget(self.props.target)
            if widget:
                    widget.props.value = str(result)
                    widget.update()
            else:
                self.app.notify(f"Widget '{self.props.target}' not found", severity="error")
                # self.app.notify(f"Command Output:\n{output}", severity="information")

    def _write_shell_script(self) -> None:
        with open('a.sh', 'w') as f:
            for w in self.app.panel.get_all_widgets():
                if w.props.name and hasattr(w.props, 'value') and w.props.name[0] != '_':
                    name = w.props.name
                    value = w.props.value
                    if w.parent != self.app.panel.container:
                        name = f"{w.parent.props.name}_{name}"
                    f.write(f'export {name}="{self._escape_value(value)}"\n')
            f.write(f'{self.props.command}\n')
    
    def _exec_shell_script(self) -> None:
        os.system(f"source a.sh 2>a.err > a.out")
        with open('a.out', 'r') as f:
            output = f.read()
            widget = self.app.panel.find_widget(self.props.target)
            if widget:
                widget.props.value = output
                widget.update()
            else:
                self.app.notify(f"Widget '{self.props.target}' not found", severity="error")
                # self.app.notify(f"Command Output:\n{output}", severity="information")
        with open('a.err', 'r') as f:
            output = f.read().strip()
            if output:
                self.app.notify(f"Command Error Output:\n{output}", severity="error")

    def on_click(self, event: "Click") -> None:
        if event.button == 3:
            event.prevent_default()
            return

        if self.props.command and not self.props.python:
            self.app.notify(f"Executing command: {self.props.command}", severity="information")
            self._write_shell_script()
            self._exec_shell_script()
        elif self.props.command and self.props.python:
            context = self._create_context()
            self._python_eval(context)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        pass
