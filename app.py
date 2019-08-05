from ansimarkup import ansiprint as print

from sarasvati.commands.command import Command, CommandException, CommandResult
from sarasvati.commands.result import (ErrorCommandLineResult,
                                       MessageCommandLineResult)


class InteractiveShellApplication:
    def __init__(self, api):
        self.__api = api

    def run(self):
        path = self.__api.config.stores.local.path
        brain = self.__api.brains.open("local://" + path + "/default")
        plugin = self.__api.plugins.get(category="CommandLine")

        prompt = ""
        while prompt != "/q":
            brain = self.__api.brains.active
            active_thought = brain.active_thought
            prompt = input(brain.name + "@" + (active_thought.title + "> " if active_thought else "> "))
            result = None
            
            try:
                result = plugin.execute(prompt)
            except CommandException as ex:
                print(f"<red>{ex.message}</red>")

            if isinstance(result, Command):
                result = result.do()

            if isinstance(result, (MessageCommandLineResult, CommandResult)):
                if isinstance(result.message, str):
                    print(result.message)
                elif isinstance(result.message, list):
                    for line in result.message:
                        print(line)
