

class Token:
    def __init__(self, tokenType, lexeme, literal, line):
        self.type = tokenType
        self.lexeme = lexeme
        self.literal = literal
        sel.line = line

    def __string__(self):
        return self.type + " " + self.lexeme + " " + self.literal
