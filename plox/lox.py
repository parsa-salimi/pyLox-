from Scanner import Scanner
import sys

class Lox:
    def __init__(self):
        self.had_error = False

    def run_file(self, file):
        f = open(file)
        self.run(f.read())
        if (self.had_error):
            sys.exit(65)
    def run_prompt(self):
        while True:
            prompt = input('>> ')
            if not prompt:
                break
            self.run(prompt)
            self.had_error = False

    def run(self, prompt):
        s = Scanner(prompt)
        tokens = s.scanTokens()
        print(tokens)

    def error(self, line, message):
        report(line, "", message)

    def report(self,line,where, message):
        print("[line" + line + "] Error" _ where + ": " + message)





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