from TokenType import TokenType

class Scanner:
    def __init__(self, source):
        self.source = source 
        self.start = 0
        self.current = 0
        self.line = 1
        self.tokens = []
    def scanTokens(self):
        while (not self.isAtEnd()):
            self.start = self.current
            scanToken(self)
        tokens.append(Token(TokenType.EOF, "", None, line))
        return tokens
    def isAtEnd(self):
        return (current >= len(self.source))
