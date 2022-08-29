from Scanner import Scanner
import sys


class ErrorHandler:
    def __init__(self):
        self.had_error = False
    def error(self, line, message):
        self.report(line, "", message)

    def report(self,line,where, message):
        print("[line" + str(line) + "] Error" + where + ": " + message)
        self.had_error = True


class Lox:
    def __init__(self):
        self.ErrorHandler = ErrorHandler()

    def run_file(self, file):
        f = open(file)
        self.run(f.read())
        if (self.ErrorHandler.had_error):
            sys.exit(65)
    def run_prompt(self):
        while True:
            prompt = input('>> ')
            if not prompt:
                break
            self.run(prompt)
            self.ErrorHandler.had_error = False

    def run(self, prompt):
        s = Scanner(prompt, self.ErrorHandler)
        tokens = s.scanTokens()
        for token in tokens:
            print(str(token))





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