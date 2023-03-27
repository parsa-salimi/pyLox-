from LoxCallable import LoxCallable

import time

def stringify(obj):
    if (obj == None) : return "nil"
    if (isinstance(obj,float)):
        text = str(obj)
        if (text.endswith(".0")) : text = text[0: len(text) - 2]
        return text
    return str(obj)

class Clock(LoxCallable):
    def arity(self):
        return 0
    def call(self, interpreter, arguments):
        return time.time()
    def __str__(self):
        return "<native fn Clock>"

class Print(LoxCallable):
    def arity(self):
        return 1
    def call(self,interpreter, arg):
            print(stringify(arg[0]))

    def __str__(self):
        return "<native fn Print>"


NativeFunctionsList = {"clock": Clock, "print" : Print}
