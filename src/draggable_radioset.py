from dataclasses import dataclass
from textual.widgets import RadioSet, RadioButton
from mixins.draggable_widget import DraggableWidget
from mixins.properties_widget import PropertiesWidget, code

@dataclass
class RadioSetProperties:
    type: str = "RadioSet"
    name: str = "radioset"
    label: str = "RadioSet"
    value: str = ""
    values: code = "a\nb\nc"
    row: int = 0
    col: int = 0
    width: int = 35
    height: int = 10
    target: str = ""

class DraggableRadioSet(DraggableWidget, PropertiesWidget, RadioSet):
    def __init__(self, props: RadioSetProperties = None, *args, **kwargs):
        if props is None:
            props = RadioSetProperties()
        self.last_values = None
        RadioSet.__init__(self, classes="draggable-radioset", *args, **kwargs)
        PropertiesWidget.__init__(self, props)
        DraggableWidget.__init__(self)
        super().update(props)

    def update(self, props=None):
        super().update(props)
        self.border_title = self.props.label

        if self.last_values != self.props.values:
            for radio in self.children:
                radio.remove()
            for value in self.props.values.split("\n"):
                self.notify(f"Adding RadioButton with value: {value}")
                radio = RadioButton(value)
                self.mount(radio)
            self.last_values = self.props.values
            self.width = self.props.width
            self.height = self.props.height
            self.refresh()
        pass

    def on_radio_button_changed(self, event: RadioButton.Changed) -> None:
        if event.value:
            self.props.value = str(event.radio_button.label)
            if self.props.target:
                target = self.app.panel.find_widget(self.props.target)
                if target:
                    target.props.value = self.props.value