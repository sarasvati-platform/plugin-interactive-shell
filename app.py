from ansimarkup import ansiprint as print
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.lexers import PygmentsLexer

from sarasvati.commands.command import Command, CommandException, CommandResult

from .aux import get_thought_path
from .prompt import PromptCompleter, PromptLexer


class InteractiveShellApplication:
    def __init__(self, api):
        self.__api = api
        
        # initialize command line
        self.__command_line = self.__api.plugins.get(category="CommandLine")
        self.__prompt_session = PromptSession(
            lexer=PygmentsLexer(PromptLexer),
            complete_while_typing=True, bottom_toolbar=self.bottom_toolbar,
            rprompt=self.rprompt)

    def bottom_toolbar(self):
        brain = self.__api.brains.active
        thought_title = brain.active_thought.title if brain.active_thought else ""
        
        #parent_title = ""
        #if brain.active_thought and len(brain.active_thought.links.parents) == 1:
        #    parent_title = brain.active_thought.links.parents[0].title
        parent_title = get_thought_path(brain.active_thought)
        parent_title = " / ".join(reversed(parent_title))

        return HTML(f'<b><style bg="ansired"> {brain.name}</style> // {parent_title}</b>')

    def rprompt(self):
        brain = self.__api.brains.active
        if not brain:
            return ""
        if not brain.active_thought:
            return ""
        if brain.active_thought.has_component("taxonomy"):
            category = brain.active_thought.taxonomy.category or ""
            tags = ", ".join(sorted(brain.active_thought.taxonomy.tags))
            return HTML(f"<style bg='#ff0066'>{category}</style> <style bg='#6600ff'>{tags}</style>")
        return ""

    def run(self):
        self.__open_brain()
        
        command = ""
        while command != "/q":
            try:
                command = self.__prompt().strip()
                if command.startswith("/"):
                    self.__execute(command)
                else:
                    self.__execute("/activate-thought " + command)
            except CommandException as ex:
                print(f"<red>{ex.message}</red>")

    def __open_brain(self, path:str = "default"):
        path = self.__api.config.stores.local.path  # todo: config may not exist
        return self.__api.brains.open("local://" + path + "/default")

    def __prompt(self):
        brain = self.__api.brains.active
        thought_title = brain.active_thought.title if brain.active_thought else ""
        return self.__prompt_session.prompt(
            f"{thought_title}> ", 
            completer=PromptCompleter(self.__command_line.get_commands(), self.__api))

    def __execute(self, command):
        result = None
        try:
            result = self.__command_line.execute(command)
        except CommandException as ex:
            print(f"<red>{ex.message}</red>")

        # if isinstance(result, Command):
        #     result = result.do()

        if isinstance(result, (CommandResult)):
            if isinstance(result.message, str):
                print(result.message)
            elif isinstance(result.message, list):
                for line in result.message:
                    print(line)
