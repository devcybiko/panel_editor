from textual.events import MouseDown, MouseUp, MouseMove

from widget_factory import WidgetFactory

RESIZING_BORDER_SIZE = 4

class DraggableWidget:    
    def __init__(self, *args, **kwargs):
        self.is_dragging = False
        self.is_resizing = False
        self.is_sizable = True
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.initial_offset_x = 0
        self.initial_offset_y = 0
        self.initial_width = 0
        self.initial_height = 0
    
    def start_dragging(self, event: MouseDown) -> None:
        self.is_dragging = True
        
        # Store the initial mouse position and current widget offset
        self.drag_start_x = event.screen_x
        self.drag_start_y = event.screen_y
        self.initial_width = self.props.width
        self.initial_height = self.props.height
        self.hit_x = event.screen_x - self.parent.props.col - self.props.col
        self.hit_y = event.screen_y - self.parent.props.row - self.props.row
        if self.is_sizable and self.hit_x > (self.props.width - RESIZING_BORDER_SIZE) and self.hit_y > (self.props.height - RESIZING_BORDER_SIZE):
            self.is_resizing = True

        # Get current offset (if any)
        current_offset = getattr(self.styles, 'offset', None)
        if current_offset is not None:
            # Handle ScalarOffset object - extract numeric values
            try:
                self.initial_offset_x = float(current_offset[0].value) if hasattr(current_offset[0], 'value') else float(current_offset[0])
                self.initial_offset_y = float(current_offset[1].value) if hasattr(current_offset[1], 'value') else float(current_offset[1])
            except (AttributeError, TypeError, IndexError):
                self.initial_offset_x = 0
                self.initial_offset_y = 0
        else:
            self.initial_offset_x = 0
            self.initial_offset_y = 0
        
        self.capture_mouse()
        event.prevent_default()
    
    async def stop_dragging(self, event: MouseUp) -> None:
        if self.is_dragging:
            self.is_dragging = False
            self.is_resizing = False
            self.release_mouse()
            
            # Check for drop into container or removal from current container
            await self.handle_drop(event)
            
            event.prevent_default()
    
    async def _move_to_container(self, container, event: MouseUp) -> None:
        await self.remove()
        container.refresh()
        new_widget = WidgetFactory.from_properties(self.props)
        await container.mount(new_widget)

        if container == self.app.container:
            new_widget.props.row = event.screen_y - self.hit_y + 2
            new_widget.props.col = event.screen_x - self.hit_x + 2
            new_widget.update()
            self.app.notify(f"'{self.props.name}' was added to APP.CONTAINER", severity="information")
        else:
            new_widget.props.row = event.screen_y - self.hit_y - container.props.row - 2
            new_widget.props.col = event.screen_x - self.hit_x - container.props.col - 2
            new_widget.update()
            self.app.notify(f"'{self.props.name}' was added to '{container.props.name}'", severity="information")

    
    async def handle_drop(self, event: MouseUp) -> None:
        """Check if widget should be added to or removed from containers"""
        if self.props.type == 'Container': return
        container = self.get_container_at_position(event.screen_x, event.screen_y)
        if container == self.parent: 
            return
        if container is None:
            if self.parent == self.app.container:
                return
            await self._move_to_container(self.app.container, event)
        else:
            await self._move_to_container(container, event)

    def get_container_at_position(self, x, y):
        containers = self.app.query(".draggable-container")
        for container in containers:
            if container == self: continue
            offset = container.styles.offset
            cx = offset[0].value
            cy = offset[1].value
            cw = container.props.width
            ch = container.props.height

            # Check if position is inside container
            if (cx <= x <= cx + cw and
                cy <= y <= cy + ch):
                return container
                
        return None
    
    def handle_drag_move(self, event: MouseMove) -> None:
        if self.is_dragging:
            # Calculate how far the mouse has moved from the start
            delta_x = event.screen_x - self.drag_start_x
            delta_y = event.screen_y - self.drag_start_y
            
            if self.is_resizing:
                self.props.width = self.initial_width + delta_x
                self.props.height = self.initial_height + delta_y
            else:
                # Apply the delta to the initial position
                new_x = self.initial_offset_x + delta_x
                new_y = self.initial_offset_y + delta_y
            
                # Update the widget's position (this will be absolute during dragging)
                self.styles.offset = (new_x, new_y)
                
                # Update properties to match new position
                self.props.col = int(new_x)
                self.props.row = int(new_y)
            
            self.update()
            event.prevent_default()

    async def on_mouse_up(self, event: MouseUp) -> None:
        if event.button == 3:
            if self.app.panel.selected_widget != self:
                return
            if self.is_dragging:
                await self.stop_dragging(event)
                self.app.panel.selected_widget = None
            else:
                self.show_properties_sheet()
            event.prevent_default()

    def on_mouse_move(self, event: MouseMove) -> None:
        if event.button == 3:
            if self.app.panel.selected_widget != self:
                return
            if self.is_dragging:
                self.handle_drag_move(event)
            else:
                self.start_dragging(event)
            event.prevent_default()

    def on_mouse_down(self, event: MouseDown) -> None:
        if event.button == 3:
            if self.app.panel.selected_widget != self:
                return
            self.start_dragging(event)
            event.prevent_default()

    def find_widget(self, name: str) -> 'DraggableWidget | None':
        return self.app.panel.find_widget(name)
