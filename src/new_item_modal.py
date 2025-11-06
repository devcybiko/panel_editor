from textual.containers import Container
from textual.widgets import Label, OptionList
from textual.widgets.option_list import Option
from textual.screen import ModalScreen
from textual.app import ComposeResult


class NewItemModal(ModalScreen):    
    CSS_PATH = "css/new_item_modal.css"
    
    def compose(self) -> ComposeResult:
        yield Container(
            Label("New Item", id="new_item_title"),
            OptionList(
                Option("Button", id="button"),
                Option("Data Table", id="datatable"),
                Option("Directory Tree", id="directorytree"),
                Option("Checkbox", id="checkbox"),
                Option("Container", id="container"),
                Option("Input", id="input"),
                Option("Label", id="label"),
                Option("RadioSet", id="radioset"),
                Option("Text Area", id="textarea"),
                Option("Tree", id="tree"),
                id="option_list"
            ),
            id="new_item_dialog"
        )
    
    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        self.dismiss(event.option.id)
    
    def on_key(self, event) -> None:
        option_list = self.query_one("#option_list", OptionList)
        keylist = "bct"
        index = keylist.find(event.key)
        if index != -1:
            option_list.highlighted = index
            event.prevent_default()
        if event.key == "escape":
            self.dismiss(None)
            event.prevent_default()