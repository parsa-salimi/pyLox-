
from ErrorHandler import ErrorHandler, LoxRuntimeError

class Environment():


    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name, value):
        self.values[name] = value

    def getAt(self, depth, name):
        return self.ancestor(depth).values.get(name)

    def assignAt(self, distance, name, value) :
        self.ancestor(distance).values[name.lexeme] = value

    def ancestor(self, depth):
        env = self
        for i in range(depth):
            env = env.enclosing
        return env

    def get(self, name):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        elif self.enclosing:
            return self.enclosing.get(name)
        else: raise LoxRuntimeError(name, "Error, undefined variable " + name.lexeme + ".")
    def assign(self, name, value):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        elif self.enclosing:
            self.enclosing.assign(name,value)
            return
        else: raise LoxRuntimeError(name, "Undefined variable " + name.lexeme + ".")
