from Scanner import Scanner
from Parser import Parser, ParseError
from astPrinter import AstPrinter
from TokenType import TokenType
from Interpreter import Interpreter
from Resolver import Resolver
import ErrorHandler
from ErrorHandler import LoxRuntimeError, ErrorHandler
import sys





class Lox:

    #def __init__(self):
    #    self.ErrorHandler = ErrorHandler()

    #ErrorHandler = ErrorHandler()
    interpreter = Interpreter()
    def run_file(self, file):
        f = open(file)
        self.run(f.read())
        if (ErrorHandler.had_error):
            sys.exit(65)
        if (ErrorHandler.hadRuntimeError) :
            sys.exit(70)
    def run_prompt(self):
        while True:
            prompt = input('>> ')
            if not prompt:
                break

            self.run(prompt)
            if ErrorHandler.had_error:
                ErrorHandler.set_error_field(False)

            #ErrorHandler.set_error_field(False)

    def runExpr(self,prompt):
        scanner = Scanner(prompt)
        tokens = scanner.scanTokens()
        parser = Parser(tokens)
        ast = parser.expression()
        if ErrorHandler.had_error : return
        resolver = Resolver(self.interpreter)
        resolver.resolveExpr(ast)
        if ErrorHandler.had_error: return
        value = self.interpreter.evaluate(ast)
        print(self.interpreter.stringify(value))
        return

    def run(self, prompt):
        scanner = Scanner(prompt)
        tokens = scanner.scanTokens()
        parser = Parser(tokens)
        statements = parser.parse()
        if ErrorHandler.had_error : return
        resolver = Resolver(self.interpreter)
        resolver.resolveStmts(statements)
        if ErrorHandler.had_error: return
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
