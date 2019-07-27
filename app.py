from ansimarkup import ansiprint as print

from sarasvati.commands.command import Command, CommandException
from sarasvati.commands.result import (ErrorCommandLineResult,
                                       MessageCommandLineResult)


class InteractiveShellApplication:
    def __init__(self, api):
        self.__api = api

    def run(self):
        brain = self.__api.brain.open("default.json")
        plugin = self.__api.plugins.get(category="CommandLine")

        prompt = ""
        while prompt != "/q":
            prompt = input("> ")
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
