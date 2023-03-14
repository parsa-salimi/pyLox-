
from ErrorHandler import ErrorHandler, LoxRuntimeError

class Environment():
    def __init__(self):
        self.values = {}
    def define(self, name, value):
        self.values[name] = value
    def get(self, name):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        else: raise LoxRuntimeError(name, "Error, undefined variable " + name.lexeme + ".")