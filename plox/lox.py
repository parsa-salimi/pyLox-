from Scanner import Scanner
from Parser import Parser
from astPrinter import AstPrinter
from TokenType import TokenType
from Interpreter import Interpreter
import sys


class ErrorHandler:
    def __init__(self):
        self.had_error = False
        self.hadRuntimeError = False
    def error(self, line, message):
        self.report(line, "", message)

    def report(self,line,where, message):
        print("[line" + str(line) + "] Error" + where + ": " + message)
        self.had_error = True

    def error(self, token, message):
        if (token.type == TokenType.EOF):
            self.report(token.line, " at end", message)
        else : self.report(token.line, " at '" + token.lexeme + "'", message)

    def runtimeError(self, err):
        print(str(err) + "\n[ line " + str(err.token.line) + "]")
        self.hadRuntimeError = True


class Lox:

    #def __init__(self):
    #    self.ErrorHandler = ErrorHandler()

    ErrorHandler = ErrorHandler()
    interpreter = Interpreter(ErrorHandler)
    def run_file(self, file):
        f = open(file)
        self.run(f.read())
        if (self.ErrorHandler.had_error):
            sys.exit(65)
        if (self.ErrorHandler.hadRuntimeError) :
            sys.exit(70)
    def run_prompt(self):
        while True:
            prompt = input('>> ')
            if not prompt:
                break
            self.run(prompt)
            self.ErrorHandler.had_error = False

    def run(self, prompt):
        scanner = Scanner(prompt, self.ErrorHandler)
        tokens = scanner.scanTokens()
        parser = Parser(tokens, self.ErrorHandler)
        statements = parser.parse()
        if self.ErrorHandler.had_error : return
        self.interpreter.interpret(statements)








def main():
    lox = Lox()
    if len(sys.argv) > 2 :
        print("Usage : plox [file]")
        sys.exit(64)
    elif len(sys.argv) == 2:
        lox.run_file(sys.argv[1])
    else:
        lox.run_prompt()

main()