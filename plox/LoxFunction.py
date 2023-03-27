from LoxCallable import LoxCallable
from Environment import Environment

class LoxFunction(LoxCallable):
    def __init__(self,declaration):
        self.declaration = declaration
    def arity(self):
        return len(self.declaration.params)
    def call(self,interpreter, args):
        env = Environment(interpreter.globalEnv)
        for i in range(len(self.declaration.params)):
            env.define(self.declaration.params[i].lexeme, args[i])
        interpreter.executeBlock(self.declaration.body, env)
        return None
    def __str__(self):
        return "<fn " + self.declaration.lexeme + ">"
