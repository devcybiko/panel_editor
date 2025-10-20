from textual.app import App, ComposeResult
from textual.containers import Horizontal, Container
from textual.widgets import Header, Button, Static

class MoverApp(App):
    """An app that moves a widget between containers."""

    CSS = """
    #left-container, #right-container {
        border: heavy $secondary;
        padding: 1;
        width: 1fr;
        height: 100%;
    }
    Horizontal {
        height: 1fr;
    }
    #movable-widget {
        background: $surface;
        color: $text;
        padding: 1;
        border: round $accent;
        height: 5;
    }
    """
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Button("Move Widget", id="move-button")
        with Horizontal():
            with Container(id="left-container"):
                yield Static("I am here now.", id="movable-widget")
            yield Container(id="right-container")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """An action to move the widget when the button is pressed."""
        if event.button.id == "move-button":
            # Query the entire app for the movable widget, ensuring it's always found
            movable_widget = self.query_one("#movable-widget")
            
            # Get references to the containers
            left_container = self.query_one("#left-container")
            right_container = self.query_one("#right-container")

            # Check which container the widget is currently in
            if movable_widget.parent == left_container:
                # 1. Await removal from the old container
                await movable_widget.remove()
                # 2. Await mounting to the new container
                await right_container.mount(movable_widget)
            else:
                # 1. Await removal from the old container
                await movable_widget.remove()
                # 2. Await mounting to the new container
                await left_container.mount(movable_widget)

if __name__ == "__main__":
    app = MoverApp()
    app.run()
