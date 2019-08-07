from ansimarkup import ansiprint as print
from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer

from sarasvati.commands.command import Command, CommandException, CommandResult

from .prompt import PromptCompleter, PromptLexer


class InteractiveShellApplication:
    def __init__(self, api):
        self.__api = api
        
        # initialize command line
        self.__command_line = self.__api.plugins.get(category="CommandLine")
        self.__prompt_session = PromptSession(
            lexer=PygmentsLexer(PromptLexer),
            completer=PromptCompleter(
                self.__command_line.get_commands(), api))

    def run(self):
        self.__open_brain()
        
        command = ""
        while command != "/q":
            try:
                command = self.__prompt()
                self.__execute(command)
            except CommandException as ex:
                print(f"<red>{ex.message}</red>")

    def __open_brain(self, path:str = "default"):
        path = self.__api.config.stores.local.path  # todo: config may not exist
        return self.__api.brains.open("local://" + path + "/default")

    def __prompt(self):
        brain = self.__api.brains.active
        thought_title = brain.active_thought.title if brain.active_thought else ""
        prompt_string = brain.name +  ("@" + thought_title + "> " if thought_title else "> ")
        return self.__prompt_session.prompt(prompt_string)

    def __execute(self, command):
        result = None
        try:
            result = self.__command_line.execute(command)
        except CommandException as ex:
            print(f"<red>{ex.message}</red>")

        if isinstance(result, Command):
            result = result.do()

        if isinstance(result, (CommandResult)):
            if isinstance(result.message, str):
                print(result.message)
            elif isinstance(result.message, list):
                for line in result.message:
                    print(line)
