from ansimarkup import ansiprint as print

from sarasvati.plugins import ApplicationPlugin
from sarasvati.commands.result import ErrorCommandLineResult, MessageCommandLineResult
from sarasvati.commands.command import Command, CommandException

class InteractiveShellApplicationPlugin(ApplicationPlugin):
    def __init__(self):
        super().__init__()

    def activate(self):
        super().activate()
        brain = self._api.brain.open("default.json")
        plugin = self._api.plugins.get(category="CommandLine")

        prompt = ""
        while prompt != "/q":
            prompt = input()
            result = None
            
            try:
                result = plugin.execute(prompt)
            except CommandException as ex:
                print(f"<red>{ex.message}</red>")
    
            if isinstance(result, Command):
                result = result.do()
                if result.message:
                    print(result.message)
            
            if isinstance(result, MessageCommandLineResult):
                if isinstance(result.message, str):
                    print(result.message)
                elif isinstance(result.message, list):
                    for line in result.message:
                        print(line)
            
    def deactivate(self):
        pass
