
from lox import ErrorHandler

class Environment():
    def __init__(self, error_handler):
        self.values = {}
        self.error_handler = error_handler
    def define(self, name, value):
        self.values[name] = value
    def get(self, name):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        else return ErrorHandler.runtimeError(name)