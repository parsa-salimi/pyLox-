from LoxCallable import LoxCallable
from Environment import Environment
from Return import Return

class LoxFunction(LoxCallable):
    def __init__(self,declaration, closure):
        self.declaration = declaration
        self.closure = closure
    def arity(self):
        return len(self.declaration.params)
    def call(self,interpreter, args):
        env = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            env.define(self.declaration.params[i].lexeme, args[i])
        try:
            interpreter.executeBlock(self.declaration.body, env)
        except Return as r:
            return r.value

        return None
    def __str__(self):
        return "<fn " + self.declaration.lexeme + ">"
