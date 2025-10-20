import json
import sys
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Button, Footer, Input
from textual.reactive import reactive
from textual.events import MouseDown
from draggable_container import ContainerProperties, DraggableContainer
from draggable_button import DraggableButton, ButtonProperties
from draggable_input import DraggableInput, InputProperties
from new_item_modal import NewItemModal
from draggable_datatable import DraggableDataTable, DataTableProperties
from draggable_textarea import DraggableTextArea, TextAreaProperties
from draggable_widget import DraggableWidget
from draggable_label import DraggableLabel, LabelProperties
from draggable_tree import DraggableTree, TreeProperties


class PanelEditor(App):    
    BINDINGS = [
        ("ctrl+n", "show_new_item_modal", "New Item"),
        ("ctrl+s", "save_panel", "Save"),
        ("ctrl+l", "load_panel", "Load"),
        ("c", "clear_buttons", "Clear All"),
        ("q", "quit", "Quit"),
    ]
    CSS_PATH = "./css/panel_editor.css"

    def compose(self) -> ComposeResult:
        yield Container(id="widget_container")
        yield Footer()

    def on_mount(self) -> None:
        self.container = self.query_one("#widget_container", Container)
        self.container.props = ContainerProperties(name="Main Container", type="Container", row=0, col=0, width=100, height=100)
        self.app.panel = self
        self.app.panel.selected_widget = None
        self.action_load_panel()

    def action_show_new_item_modal(self) -> None:
        def handle_selection(selection):
            if selection == "button":
                new_widget = DraggableButton()
            elif selection == "container":
                new_widget = DraggableContainer()
            elif selection == "datatable":
                new_widget = DraggableDataTable()
            elif selection == "label":
                new_widget = DraggableLabel()
            elif selection == "input":
                new_widget = DraggableInput()
            elif selection == "textarea":
                new_widget = DraggableTextArea()
            elif selection == "tree":
                new_widget = DraggableTree()
            else:
                return
            if self.container.children:
                self.container.mount(new_widget, before=self.container.children[0])
            else:
                self.container.mount(new_widget)
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
        with open("a.json", "w") as f:
            json.dump(widgets_data, f, indent=2)
            f.flush()  # Ensure data is written to disk
        self.notify("File saved to a.json", severity="information")

    def load_widgets(self, widgets_data, container) -> None:
        for widget_data in widgets_data:
            if widget_data["type"] == "Button":
                props = ButtonProperties(**widget_data)
                widget = DraggableButton(props)
                container.mount(widget)
            elif widget_data["type"] == "DataTable":
                props = DataTableProperties(**widget_data)
                widget = DraggableDataTable(props)
                container.mount(widget)
            elif widget_data["type"] == "Input":
                props = InputProperties(**widget_data)
                widget = DraggableInput(props)
                container.mount(widget)
            elif widget_data["type"] == "Label":
                props = LabelProperties(**widget_data)
                widget = DraggableLabel(props)
                container.mount(widget)
            elif widget_data["type"] == "TextArea":
                props = TextAreaProperties(**widget_data)
                widget = DraggableTextArea(props)
                container.mount(widget)
            elif widget_data["type"] == "Tree":
                props = TreeProperties(**widget_data)
                widget = DraggableTree(props)
                container.mount(widget)
            elif widget_data["type"] == "Container":
                children = widget_data.get("children", [])
                del widget_data["children"]
                props = ContainerProperties(**widget_data)
                widget = DraggableContainer(props)
                container.mount(widget)
                self.load_widgets(children, widget)

    def action_load_panel(self) -> None:
        with open("a.json", "r") as f:
            panel_data = json.load(f)
        self.action_remove_all_widgets()
        widgets = panel_data.get("children", [])
        self.load_widgets(widgets, self.container)
        self.notify(f"Loaded {len(widgets)} widgets from a.json", severity="information")

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
                    if child.props.name == f"{widget.props.name}.{name}":
                        return child
        return None

    def action_remove_all_widgets(self) -> None:
        for widget in self.container.query("*"):
            if widget.props: widget.remove()
    
    def on_mouse_down(self, event: MouseDown) -> None:
        if event.button == 3:  # Right click
            result = self.get_widget_at(*event.screen_offset)
            if not result: return
            widget, region = result
            if not widget: return
            if widget.id == "widget_container":
                self.action_show_new_item_modal()
            else:
                self.selected_widget = widget
            event.prevent_default()


    def on_input_changed(self, event: Input.Changed) -> None:
        pass

    def to_back(self, widget) -> None:
        """Move the specified widget to the back of the container's children."""
        if widget in self.container.children:
            self.container.remove(widget)
            self.container.mount(widget, before=self.container.children[0])



app = PanelEditor()

def main():
    app.run()

if __name__ == "__main__":
    main()