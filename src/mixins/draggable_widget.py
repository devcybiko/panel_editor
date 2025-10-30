from textual.events import MouseDown, MouseUp, MouseMove, Click

from mixins.logging_widget import LoggingWidget
from mixins.menu_widget import MenuWidget
from widget_factory import WidgetFactory

RESIZING_BORDER_SIZE = 4
X_PADDING = 2
Y_PADDING = 2

class DraggableWidget(LoggingWidget, MenuWidget):    
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
    
    @property
    def x(self) -> int:
        return int(self.styles.offset[0].value)

    @property
    def y(self) -> int:
        return int(self.styles.offset[1].value)
    
    @property
    def abs_x(self) -> int:
        return self.x + self.parent.props.col + X_PADDING

    @property
    def abs_y(self) -> int:
        return self.y + self.parent.props.row + Y_PADDING

    @property
    def row(self) -> int:
        return self.y

    @property
    def col(self) -> int:
        return self.x

    async def start_dragging(self, event: MouseDown) -> None:
        self = await self._move_to_container(self.app.container, event)
        self.is_dragging = True
        self.capture_mouse()
        
        # Store the initial mouse position and current widget offset
        self.drag_start_x = event.screen_x
        self.drag_start_y = event.screen_y
        self.initial_width = self.props.width
        self.initial_height = self.props.height
        self.hit_x = event.screen_x - self.parent.props.col - self.props.col
        self.hit_y = event.screen_y - self.parent.props.row - self.props.row
        if self.is_sizable and self.hit_x > (self.props.width - RESIZING_BORDER_SIZE) and self.hit_y > (self.props.height - RESIZING_BORDER_SIZE):
            self.is_resizing = True

        self.initial_offset_x = self.x
        self.initial_offset_y = self.y

    async def to_front(self):
        self.parent.move_child(self, before=-1)

    async def to_back(self):
        self.parent.move_child(self, before=0)

    async def stop_dragging(self, event: MouseUp) -> None:
        if self.is_dragging:
            self.is_dragging = False
            self.is_resizing = False
            self.release_mouse()
            await self.handle_drop(event)
                
    async def _move_to_container(self, container, event: MouseUp) -> None:
        if self.props.type == 'Container':
            return self
        if self.parent == container:
            return self  # No change needed
        if container == self.app.container:
            self.props.row = self.abs_y
            self.props.col = self.abs_x
        else:
            self.props.row = self.abs_y - container.props.row - Y_PADDING * 2
            self.props.col = self.abs_x - container.props.col - X_PADDING * 2
        new_widget = WidgetFactory.from_properties(self.props)
        await self.remove()
        await container.mount(new_widget, before=container.children[-1])
        await self.to_front()
        container.refresh()
        return new_widget


    async def handle_drop(self, event: MouseUp) -> None:
        """Check if widget should be added to or removed from containers"""
        if self.props.type == 'Container':
            # containers cannot be nested
            return
        if self.parent == self.app.container:
            # we're dropping from app container into draggable_container
            # use upper-left corner of widget
            container = self.get_container_at_position(self.abs_x, self.abs_y)
            if container != None:
                await self._move_to_container(container, event)
        else:
            # removing from a container - alows drop back onto app container (never drop into another container)
            await self._move_to_container(self.app.container, event)

    def get_container_at_position(self, x, y):
        containers = self.app.query(".draggable-container")
        for container in containers:
            if container == self: continue
            cx = container.x
            cy = container.y
            cw = container.props.width
            ch = container.props.height

            # Check if position is inside container
            if (cx + 2 <= x <= cx + cw - 2 and
                cy + 2 <= y <= cy + ch - 2):
                return container
                
        return None
    
    async def handle_drag_move(self, event: MouseMove) -> None:
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

    async def on_menu_down(self, event: MouseDown) -> None:
        await self.to_front()

    async def on_mouse_down(self, event: MouseDown) -> None:
        if event.button == 1 and event.shift:
            index = self.parent.children.index(self)
            if index == 0:
                await self.to_front()
            else:
                await self.to_back()

    async def on_menu_up(self, event: MouseUp) -> None:
        if self.is_dragging:
            await self.stop_dragging(event)
        else:
            self.show_properties_sheet()

    async def on_menu_move(self, event: MouseMove) -> None:
        if self.is_dragging:
            await self.handle_drag_move(event)
        else:
            await self.start_dragging(event)

    def find_widget(self, name: str) -> 'DraggableWidget | None':
        return self.app.panel.find_widget(name)
