class Token:
    def __init__(self, type, lexeme, literal, line):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        sel.line = line

    def __string__(self):
        return self.type + " " + self.lexeme + " " + self.literal
