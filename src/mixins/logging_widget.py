class LoggingWidget:
    def _debug(self, msg) -> None:
        if self.app.debug_mode:
            self.app.notify(msg, title="Debug", severity="debug")
    def _info(self, msg) -> None:
        self.app.notify(msg, title="Info", severity="information")
    def _warning(self, msg) -> None:
        self.app.notify(msg, title="Warning", severity="warning")
    def _error(self, msg) -> None:
        self.app.notify(msg, title="Error", severity="error")
