from dataclasses import fields
from textual.containers import Container, Horizontal
from textual.widgets import Button, Label, TextArea, Checkbox, Input
from textual.screen import ModalScreen
from textual.app import ComposeResult

from mixins.menu_widget import MenuWidget

class PropertiesSheet(MenuWidget, ModalScreen):    
    CSS_PATH = "css/properties_sheet.css"
    
    def __init__(self, widget_to_edit, title: str):
        super().__init__()
        self.widget_to_edit = widget_to_edit
        self.title = title
    
    def compose(self) -> ComposeResult:
        from mixins.properties_widget import text, code

        ## props is guaranteed to be non-null
        props = self.widget_to_edit.props
        content_widgets = []
        
        for field in fields(props):
            field_value = getattr(props, field.name)
            label = Label(f"{field.name.title()}:", classes="property-label")
            
            # Make "type" field read-only by using a disabled input
            if field.name.lower() in ["type"]:
                input_widget = Input(disabled=True, classes="property-input readonly-field", id=f"{field.name}_input")
                input_widget.value = str(field_value)
            elif field.type == text:
                input_widget = TextArea(classes="property-textarea-command", id=f"{field.name}_input")
                input_widget.text = str(field_value)
            elif field.type == code:
                if hasattr(props, "python") and props.python:
                    language = "python"
                else:
                    language = "bash"
                input_widget = TextArea.code_editor(classes="property-textarea-command", id=f"{field.name}_input")
                # input_widget = TextArea.code_editor(language=language, classes="property-textarea-command", id=f"{field.name}_input")
                input_widget.text = str(field_value)
            elif field.type == bool:
                # For boolean fields, use a checkbox input
                input_widget = Checkbox(value=field_value, id=f"{field.name}_input")
            else:
                input_widget = Input(id=f"{field.name}_input", classes="property-input")
                input_widget.value = str(field_value)
            
            # Put label and input side by side in a horizontal container
            content_widgets.append(Horizontal(label, input_widget, classes="property-row"))
                
        # Structure: main container with scrollable content and fixed buttons
        yield Container(
            Container(*content_widgets, id="property_content"),
            Horizontal(
                Button("OK", id="ok_btn", variant="primary"),
                Button("Cancel", id="cancel_btn", variant="default"),
                Button("Clone", id="clone_btn", variant="default"),
                Button("Delete", id="delete_btn", variant="default"),
                id="property_buttons"
            ),
            id="property_dialog"
        )
    
    def _update_props(self):
        from mixins.properties_widget import text, code
        result = {}
        props = getattr(self.widget_to_edit, 'props', None)
        if not props:
            return result
        for field in fields(props):
            # Skip the "type" field since it's read-only and doesn't have an input widget
            if field.name.lower() == "type":
                result[field.name] = getattr(props, field.name)  # Keep original value
                continue
                
            input_widget = self.query_one(f"#{field.name}_input")
            try:
                if field.type == int:
                    result[field.name] = int(input_widget.value)
                elif field.type == str:
                    result[field.name] = input_widget.value
                elif field.type == bool:
                    result[field.name] = bool(input_widget.value)
                elif field.type in [code, text]:
                    result[field.name] = input_widget.text
                else:
                    result[field.name] = input_widget.value
            except ValueError:
                result[field.name] = input_widget.value 
        return result
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "ok_btn":
            result = self._update_props()
            self.dismiss(result)
        elif event.button.id == "cancel_btn":
            self.dismiss(None)
        elif event.button.id == "clone_btn":
            self.widget_to_edit.clone_and_mount()
            self.dismiss(None)
        elif event.button.id == "delete_btn":
            self.widget_to_edit.remove()
            self.dismiss(None)