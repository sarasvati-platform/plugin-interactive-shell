from sarasvati.plugins import ApplicationPlugin

from .app import InteractiveShellApplication


class InteractiveShellApplicationPlugin(ApplicationPlugin):
    def __init__(self):
        super().__init__()

    def activate(self):
        super().activate()
        app = InteractiveShellApplication(self._api)
        app.run()
