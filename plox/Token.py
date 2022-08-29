

class Token:
    def __init__(self, tokenType, lexeme, literal, line):
        self.type = tokenType
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return str(self.type) + " " + str(self.lexeme) + " " + str(self.literal)
