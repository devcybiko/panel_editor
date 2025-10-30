from textual.events import MouseDown, MouseUp, MouseMove, Click, Enter, Leave

class MenuWidget:
    # class variable indicating menu_button_state
    menu_button_state = False
    async def on_menu_down(self, event: MouseDown) -> None:
        MenuWidget.menu_button_state = True
        pass

    async def on_menu_up(self, event: MouseUp) -> None:
        MenuWidget.menu_button_state = False
        pass

    async def on_menu_move(self, event: MouseMove) -> None:
        pass

    async def on_menu_click(self, event: Click) -> None:
        pass

    async def on_click(self, event: Click) -> None:
        if event.button == 3:
            event.stop()
            event.prevent_default()
            await self.on_menu_click(event)

    async def on_mouse_down(self, event: MouseDown) -> None:
        if event.button == 3:
            event.stop()
            event.prevent_default()
            await self.on_menu_down(event)

    async def on_mouse_up(self, event: MouseUp) -> None:
        if event.button == 3:
            event.stop()
            event.prevent_default()
            await self.on_menu_up(event)

    async def on_mouse_move(self, event: MouseMove) -> None:
        if event.button == 3:
            event.stop()
            event.prevent_default()
            await self.on_menu_move(event)

    async def on_menu_enter(self, event: MouseMove) -> None:
        if event.button == 3:
            event.stop()
            event.prevent_default()
            await self.on_menu_enter(event)

    async def on_menu_leave(self, event: MouseMove) -> None:
        if event.button == 3:
            event.stop()
            event.prevent_default()
            await self.on_menu_leave(event)

    async def on_enter(self, event: Enter) -> None:
        if MenuWidget.menu_button_state:
            event.stop()
            event.prevent_default()
            await self.on_menu_enter(event)

    async def on_leave(self, event: Leave) -> None:
        if MenuWidget.menu_button_state:
            event.stop()
            event.prevent_default()
            await self.on_menu_enter(event)

