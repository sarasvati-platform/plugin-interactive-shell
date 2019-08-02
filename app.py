from ansimarkup import ansiprint as print

from sarasvati.commands.command import Command, CommandException, CommandResult
from sarasvati.commands.result import (ErrorCommandLineResult,
                                       MessageCommandLineResult)


class InteractiveShellApplication:
    def __init__(self, api):
        self.__api = api

    def run(self):
        path = self.__api.config.brains.path
        brain = self.__api.brain.open("local://" + path + "/default/brain.json")
        plugin = self.__api.plugins.get(category="CommandLine")

        prompt = ""
        while prompt != "/q":
            active_thought = brain.active_thought
            prompt = input(active_thought.title + "> " if active_thought else "> ")
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
