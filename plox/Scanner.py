from TokenType import TokenType
from Token import Token
import ErrorHandler
from ErrorHandler import LoxRuntimeError, ErrorHandler

class Scanner:
    def __init__(self, source):
        self.source = source
        #self.error_handler = error_handler
        self.start = 0
        self.current = 0
        self.line = 1
        self.tokens = []
    def scanTokens(self):
        while (not self.isAtEnd()):
            self.start = self.current
            self.scanToken()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    keywords = {
        "and" : TokenType.AND,
        "class" : TokenType.CLASS,
        "else" : TokenType.ELSE,
        "false" : TokenType.FALSE,
        "for" : TokenType.FOR,
        "fun" : TokenType.FUN,
        "if" : TokenType.IF,
        "nil" : TokenType.NIL,
        "or" : TokenType.OR,
        "return" : TokenType.RETURN,
        "super" : TokenType.SUPER,
        "this" : TokenType.THIS,
        "true" : TokenType.TRUE,
        "var" : TokenType.VAR,
        "while" : TokenType.WHILE
    }

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
        elif (c == '!'):
            self.addToken(TokenType.BANG_EQUAL if self.match('=')  else TokenType.BANG)
        elif (c == '='):
            self.addToken(TokenType.EQUAL_EQUAL if self.match('=')  else TokenType.EQUAL)
        elif (c == '<'):
            self.addToken(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
        elif (c == '>'):
            self.addToken(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
        elif (c == '/'):
            if (self.match('/')):
                while (self.peek() != '\n' and (not (self.isAtEnd()))) : self.advance()
            else:
                self.addToken(TokenType.SLASH)
        elif ( (c == '\t') or (c == ' ') or (c == '\r')):
            pass
        elif (c == '\n'):
            self.line += 1
        elif (c == '"'): self.string()
        elif (c.isdigit()): self.number()
        elif (c.isalpha() or c=='_'): self.identifier()
        else: ErrorHandler.error(self.line, "Unexpected character")

    def isAtEnd(self):
        return (self.current >= len(self.source))

    def advance(self):
        self.current += 1
        return self.source[self.current-1]

    def match(self, expected):
        if (self.isAtEnd()) : return False
        if (self.source[self.current] != expected) : return False
        self.current += 1
        return True

    def addToken(self, tokenType):
        self.addTokenl(tokenType, None)

    def addTokenl(self, tokenType, literal):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(tokenType, text, literal, self.line))

    def peek(self):
        if (self.isAtEnd()) : return '\0'
        else :  return self.source[self.current]

    def peekNext(self):
        if (self.current + 1 >= len(self.source)) : return '\0'
        return self.source[self.current + 1]

    def string(self):
        while (self.peek() != '"' and (not self.isAtEnd())):
            if (self.peek() == '\n') : self.line += 1
            self.advance()
        if (self.isAtEnd()) :
            ErrorHandler.error(self.line, "undetermined string.")
            return
        self.advance()
        value = self.source[self.start+1 : self.current - 1]
        self.addTokenl(TokenType.STRING, value)

    def number(self):
        while (self.peek().isdigit()) : self.advance()
        if (self.peek() == '.' and self.peekNext().isdigit()) : self.advance()
        while (self.peek().isdigit()): self.advance()
        self.addTokenl(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def identifier(self):
        while (self.peek().isalpha() or self.peek().isdigit() or self.peek()=='_'): self.advance()
        text = self.source[self.start:self.current]
        identifierType = self.keywords.get(text, TokenType.IDENTIFIER)
        self.addToken(identifierType)
