from textual.containers import Container
from textual.widgets import Label, OptionList
from textual.widgets.option_list import Option
from textual.screen import ModalScreen
from textual.app import ComposeResult


class NewItemModal(ModalScreen):    
    CSS = """
    NewItemModal {
        align: center middle;
        background: rgba(0, 0, 0, 0.5);
    }
    
    #new_item_dialog {
        grid-size: 1;
        grid-gutter: 1;
        grid-rows: auto 1fr;
        padding: 1;
        width: 40;
        height: 15;
        border: solid $primary;
        background: $surface;
    }
    
    #new_item_title {
        width: 100%;
        text-align: center;
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
    }
    
    OptionList {
        width: 100%;
        height: 100%;
        border: none;
        background: $surface;
    }
    
    OptionList > .option-list--option {
        background: $surface;
        border: none;
    }
    
    OptionList > .option-list--option-highlighted {
        background: $accent;
        color: $text;
        border: none;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Container(
            Label("New Item", id="new_item_title"),
            OptionList(
                Option("Button", id="button"),
                Option("Data Table", id="datatable"),
                Option("Container", id="container"),
                Option("Label", id="label"),
                Option("Text Area", id="textarea"),
                Option("Text Input", id="input"),
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