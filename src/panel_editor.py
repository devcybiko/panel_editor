import json
import re
import sys
import os
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widget import Widget
from textual.widgets import Button, Footer, Input, RadioSet, RadioButton
from rich.text import Text
from textual.reactive import reactive
from textual.events import MouseDown
from draggable_container import ContainerProperties, DraggableContainer
from draggable_button import DraggableButton, ButtonProperties
from draggable_input import DraggableInput, InputProperties
from draggable_checkbox import DraggableCheckbox, CheckboxProperties
from new_item_modal import NewItemModal
from draggable_datatable import DraggableDataTable, DataTableProperties
from draggable_directory_tree import DraggableDirectoryTree, DirectoryTreeProperties
from draggable_textarea import DraggableTextArea, TextAreaProperties
from mixins.draggable_widget import DraggableWidget
from draggable_label import DraggableLabel, LabelProperties
from draggable_tree import DraggableTree, TreeProperties
from draggable_radioset import DraggableRadioSet, RadioSetProperties
from mixins.logging_widget import LoggingWidget
from mixins.menu_widget import MenuWidget

## GLS - HACK - monkey patch notify to add timeout default
original_notify = Widget.notify
def global_notify(self, message, timeout=5, **kwargs):
    return original_notify(self, message, timeout=timeout, **kwargs)
Widget.notify = global_notify

class PanelEditor(LoggingWidget, MenuWidget, App):    
    BINDINGS = [
        ("ctrl+n", "show_new_item_modal", "New Item"),
        ("ctrl+s", "save_panel", "Save"),
        ("ctrl+l", "load_panel", "Load"),
        ("c", "clear_buttons", "Clear All"),
        ("q", "quit", "Quit"),
    ]
    CSS_PATH = [
        "css/draggable_button.css",
        "css/draggable_checkbox.css",
        "css/draggable_directory_tree.css",
        "css/draggable_datatable.css",
        "css/draggable_input.css",
        "css/draggable_label.css",
        "css/draggable_radioset.css",
        "css/draggable_textarea.css",
        "css/draggable_tree.css",
        "css/panel_editor.css",
    ]
    remove_queue = []

    def __init__(self, filename="a.json"):
        super().__init__()
        self.filename = filename

    def compose(self) -> ComposeResult:
        yield Container(id="widget_container")
        yield Footer()

    def on_mount(self) -> None:
        self.app.debug_mode = True
        self.container = self.query_one("#widget_container", Container)
        self.container.props = ContainerProperties(name="Main Container", type="Container", row=0, col=0, width=100, height=100)
        self.app.panel = self
        self.app.panel.selected_widget = None
        self.action_load_panel()
        self.set_interval(0.25, self.heartbeat)  # Calls heartbeat every 0.5 seconds

    async def heartbeat(self) -> None:
        # Update widgets here
        for widget in self.remove_queue:
            # GLS - NOTE: this solves a problem where removing a widget during drag-and-drop causes issues
            # rather than removing widgets during event handlers we defer removal to here
            widget.remove()
        self.remove_queue = []
        for widget in self.container.children:
            widget.update()

    def action_show_new_item_modal(self) -> None:
        def handle_selection(selection):
            if selection == "button":
                new_widget = DraggableButton()
            elif selection == "checkbox":
                new_widget = DraggableCheckbox()
            elif selection == "container":
                new_widget = DraggableContainer()
            elif selection == "datatable":
                new_widget = DraggableDataTable()
            elif selection == "directorytree":
                new_widget = DraggableDirectoryTree()
            elif selection == "label":
                new_widget = DraggableLabel()
            elif selection == "input":
                new_widget = DraggableInput()
            elif selection == "radioset":
                new_widget = DraggableRadioSet()
            elif selection == "textarea":
                new_widget = DraggableTextArea()
            elif selection == "tree":
                new_widget = DraggableTree()
            else:
                self._warning(f"Unknown widget type: {selection}")
                return
            if self.container.children:
                self.container.mount(new_widget, before=self.container.children[-1])
            else:
                self.container.mount(new_widget)
        if self.screen_stack and isinstance(self.screen_stack[-1], NewItemModal):
            return  # Modal is already open, do nothing
        self.push_screen(NewItemModal(), handle_selection)

    def container_to_dict(self, container) -> None:
        container_dict = container.props.__dict__.copy()
        container_dict["children"] = []
        for widget in container.children:
            if widget.props.type == "Container":
                container_dict["children"].append(self.container_to_dict(widget))
            else:
                prop_dict = widget.props.__dict__.copy()
                if widget.props.name and widget.props.name[0] == "_" and "value" in prop_dict:
                    prop_dict["value"] = ""
                container_dict["children"].append(prop_dict)
        return container_dict

    def action_save_panel(self) -> None:
        widgets_data = self.container_to_dict(self.container)        
        with open(self.filename, "w") as f:
            json.dump(widgets_data, f, indent=2)
            f.flush()  # Ensure data is written to disk
        self._info(f"File saved to {self.filename}")

    def load_widgets(self, widgets_data, container) -> None:
        for widget_data in widgets_data:
            if widget_data["type"] == "Button":
                props = ButtonProperties(**widget_data)
                widget = DraggableButton(props)
                container.mount(widget)
            elif widget_data["type"] == "Checkbox":
                props = CheckboxProperties(**widget_data)
                widget = DraggableCheckbox(props)
                container.mount(widget)
            elif widget_data["type"] == "Container":
                children = widget_data.get("children", [])
                del widget_data["children"]
                props = ContainerProperties(**widget_data)
                widget = DraggableContainer(props)
                container.mount(widget)
                self.load_widgets(children, widget)
            elif widget_data["type"] == "DataTable":
                props = DataTableProperties(**widget_data)
                widget = DraggableDataTable(props)
                container.mount(widget)
            elif widget_data["type"] == "DirectoryTree":
                props = DirectoryTreeProperties(**widget_data)
                widget = DraggableDirectoryTree(props)
                container.mount(widget)
            elif widget_data["type"] == "Input":
                props = InputProperties(**widget_data)
                widget = DraggableInput(props)
                container.mount(widget)
            elif widget_data["type"] == "Label":
                props = LabelProperties(**widget_data)
                widget = DraggableLabel(props)
                container.mount(widget)
            elif widget_data["type"] == "RadioSet":
                props = RadioSetProperties(**widget_data)
                widget = DraggableRadioSet(props)
                container.mount(widget)
            elif widget_data["type"] == "TextArea":
                props = TextAreaProperties(**widget_data)
                widget = DraggableTextArea(props)
                container.mount(widget)
            elif widget_data["type"] == "Tree":
                props = TreeProperties(**widget_data)
                widget = DraggableTree(props)
                container.mount(widget)
            else:
                self._warning(f"Unknown widget type: {widget_data['type']}")
        container.refresh()

    def action_load_panel(self) -> None:
        with open(self.filename, "r") as f:
            panel_data = json.load(f)
        self.action_remove_all_widgets()
        widgets = panel_data.get("children", [])
        self.load_widgets(widgets, self.container)
        self._info(f"Loaded {len(widgets)} widgets from {self.filename}")

    def get_all_widgets(self) -> list:
        all_widgets = []
        for widget in self.container.children:
            if widget.children:
                for child in widget.children:
                    all_widgets.append(child)
            all_widgets.append(widget)
        return all_widgets

    def find_widget(self, name: str) -> DraggableWidget | None:
        for widget in self.container.children:
            if widget.props.name == name:
                return widget
            if widget.props.type == "Container":
                for child in widget.children:
                    if child.props.name == f"{name}":
                        return child
        return None

    def action_remove_all_widgets(self) -> None:
        for widget in self.container.query("*"):
            if widget.props: widget.remove()
    
    async def on_menu_click(self, event: MouseDown) -> None:
        self.action_show_new_item_modal()

    def to_back(self, widget) -> None:
        """Move the specified widget to the back of the container's children."""
        if widget in self.container.children:
            self.container.remove(widget)
            self.container.mount(widget, before=self.container.children[0])
    def validate_form(self) -> bool:
        """Validate all widgets marked for form validation."""
        valid = True
        for widget in self.get_all_widgets():
            if not hasattr(widget, "props"): continue
            if not hasattr(widget.props, 'regex'): continue
            if not hasattr(widget.props, "regex"): continue
            pattern = widget.props.regex
            value = getattr(widget.props, 'value', '')
            if not re.match(pattern, value):
                self.notify(f"Validation failed for '{widget.props.name}': Value '{value}' does not match pattern '{pattern}'", severity="error")
                valid = False
        return valid
def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="Panel Editor")
    parser.add_argument("filename", nargs="?", default="./apps/a.json", help="Panel file to edit (default: a.json)")
    return parser.parse_args()

def main():
    args = parse_args()
    # If the file does not exist, create it with an empty dict
    if not os.path.exists(args.filename):
        with open(args.filename, "w") as f:
            json.dump({}, f)
    app = PanelEditor(args.filename)
    app.run()

if __name__ == "__main__":
    main()