from dataclasses import dataclass
from textual.widgets import Checkbox
from mixins.draggable_widget import DraggableWidget
from mixins.properties_widget import PropertiesWidget

@dataclass
class CheckboxProperties:
    type: str = "Checkbox"
    name: str = "checkbox"
    label: str = "Checkbox"
    value: str = "yes"
    true_value: str = "yes"
    false_value: str = "no"
    row: int = 0
    col: int = 0
    width: int = 5
    height: int = 3
    border: bool = False
    variable_width: bool = True

class DraggableCheckbox(DraggableWidget, PropertiesWidget, Checkbox):
    def __init__(self, props: CheckboxProperties = None, *args, **kwargs):
        if props is None:
            props = CheckboxProperties()
        Checkbox.__init__(self, classes="draggable-checkbox-border", *args, **kwargs)
        PropertiesWidget.__init__(self, props)
        DraggableWidget.__init__(self)
        self.is_sizable = False
        self.props.width = len(self.props.label) + 7
        self.update()

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        if event.value:
            self.props.value = self.props.true_value
        else:
            self.props.value = self.props.false_value

    def update(self, props=None):
        if self.props.variable_width:
            self.props.width = len(self.props.label) + 7
        super().update(props)
        # Ensure checkbox state matches props.value
        if self.props.border:
            if "draggable-checkbox-border" not in self.classes:
                self.classes = "draggable-checkbox-border" # Restores border
        else:
            if "draggable-checkbox-no-border" not in self.classes:
                self.classes = "draggable-checkbox-no-border" # Removes border
        pass