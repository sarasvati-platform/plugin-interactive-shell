from sarasvati.plugins import ApplicationPlugin

from .app import InteractiveShellApplication


class InteractiveShellApplicationPlugin(ApplicationPlugin):
    def __init__(self):
        super().__init__()

    def check_dependencies(self, api):
        command_lines = api.plugins.find(category="CommandLine")
        if not command_lines:
            raise Exception("Sarasvati Interactive Shell requires 'CommandLine' plugin.")
        if len(command_lines) > 1:
            raise Exception("Too many 'CommandLine' plugins registered.")


    def activate(self):
        super().activate()
        app = InteractiveShellApplication(self._api)
        app.run()
