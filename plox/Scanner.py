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
        tokens.append(Token(TokenType.EOF, "", None, self.line))
        return tokens
    def isAtEnd(self):
        return (self.current >= len(self.source))
    def scanToken(self):
        c = self.advance()
        if (c == '(') : self.addToken(TokenType.LEFT_PAREN)
        elif (c == ')') : self.addToken(TokenType.RIGHT_PAREN)
        elif (c == '{') : self.addToken(TokenType.LEFT_BRACE)
        elif (c == '}') : self.addToken(TokenType.RIGHT_BRACE)
        elif (c == ',') : self.addToken(TokenType.COMMA)
        elif (c == '.') : self.addToken(TokenType.DOT)
        elif (c == '-') : self.addToken(TokenType.MINUS)
        elif (c == '+') : self.addToken(TokenType.PLUS)
        elif (c == ';') : self.addToken(TokenType.SEMICOLON)
        elif (c == '*') : self.addToken(TokenType.STAR)
        else: Lox.error(self.line, "Unexpected character")

    def advance(self):
        self.current += 1
        return self.source[self.current]
    
    def addToken(self, tokenType):
        self.addToken(tokenType, None)
    
    def addToken(self, tokenType, literal):
        text = self.source[self.start : self.current]
        tokens.append(Token(tokenType, text, literal, self.line))



