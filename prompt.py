from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document
from pygments.lexer import RegexLexer
from pygments.token import Keyword, Operator
from prompt_toolkit.formatted_text import HTML


class PromptLexer(RegexLexer):
    tokens = {
        'root': [
            (r'/(\w|-)*', Keyword),
            (r'(\w*):', Operator)
        ]
    }

class PromptCompleter(Completer):
    def __init__(self, commands, api):
        self.__commands = commands
        self.__mode = ""
        self.__start = 0
        self.__api = api

    def get_completions(self, document, complete_event):
        self.__switch_state(document)

        if self.__mode is "command":
            commands = {c: i for c, i in self.__commands.items() if document.text in c}
            for command, info in commands.items():
                yield Completion(command, 
                    start_position=-len(document.text), 
                    display_meta=info.description)

        if self.__mode in ["arg", ""]:
            text = document.text[self.__start:]
            if len(text) >= 2:
                thoughts = self.__api.brains.active.find_thoughts({
                    "field": "definition.title",
                    "operator": "~~",
                    "value": text
                })
                for thought in thoughts:
                    path = self.__get_thought_path(thought, [])
                    path = " / ".join(path[1:])
                    category = ""
                    if thought.has_component("taxonomy"):
                        category = "("+thought.taxonomy.category+")"
                    meta = HTML(f'{path} <style bg="#ff0066">{category}</style>')
                    yield Completion(thought.title, start_position=-len(text), display_meta=meta)

    def __get_thought_path(self, thought, path):
        if not thought:
            return []
        if len(path) >=3:
            return path

        path.append(thought.title)

        if len(thought.links.parents) == 1:
            parent = thought.links.parents[0]
            return self.__get_thought_path(parent, path)
        elif len(thought.links.references) == 1:
            parent = thought.links.references[0]
            return self.__get_thought_path(parent, path)
        else:
            return path

    def __switch_state(self, document: Document):
        if ("/" not in document.text) and (self.__mode is not ""):
            self.__mode = ""
            self.__start = 0

        if document.char_before_cursor is "/":
            self.__mode = "command"
            self.__start = document.cursor_position

        if document.char_before_cursor is ":":
            self.__mode = "arg"
            self.__start = document.cursor_position

        if "/" in document.text and document.char_before_cursor is " ":
            self.__mode = "arg"
            self.__start = document.cursor_position
