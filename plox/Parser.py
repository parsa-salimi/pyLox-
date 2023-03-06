from TokenType import TokenType
import Expr
import Stmt

class ParseError(Exception):
    pass

class Parser:
    def __init__(self, tokens, error_handler):
        self.tokens = tokens
        self.current = 0
        self.statements = []
        self.error_handler = error_handler

    def parse(self):
        while(not (self.isAtEnd())):
            self.statements.append(self.statement())
        return self.statements

    def statement(self):
        if(self.match([TokenType.PRINT])):
            return self.printStatement()
        else return self.expressionStatement()

    def printStatement(self):
        value=self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ; after value")
        return Stmt.Print(value)

    def expressionStatement(self):
        value=self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ; after expression")
        return Stmt.Expression(value)

    def expression(self): return self.equality()

    def equality(self):
        expr = self.comparison()
        while(self.match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL])):
            operator = self.previous()
            right = self.comparison()
            expr = Expr.Binary(expr, operator, right)
        return expr

    def comparison(self):
        expr = self.term()
        while(self.match([TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL])):
            operator = self.previous()
            right = self.term()
            expr = Expr.Binary(expr, operator, right)
        return expr

    def term(self):
        expr = self.factor()
        while(self.match([TokenType.MINUS, TokenType.PLUS])):
            operator = self.previous()
            right = self.factor()
            expr = Expr.Binary(expr, operator, right)
        return expr


    def factor(self):
        expr = self.unary()
        while(self.match([TokenType.SLASH, TokenType.STAR])):
            operator = self.previous()
            right = self.unary()
            expr = Expr.Binary(expr, operator, right)
        return expr

    def unary(self):
        if (self.match([TokenType.BANG, TokenType.MINUS])):
            operator = self.previous()
            right = self.unary()
            return Expr.Unary(operator, right)
        return self.primary()

    def primary(self):
        if self.match([TokenType.FALSE]) : return Expr.Literal(False)
        if self.match([TokenType.TRUE]) : return Expr.Literal(True)
        if self.match([TokenType.NIL]) : return Expr.Literal(None)
        if self.match([TokenType.NUMBER, TokenType.STRING]): return Expr.Literal(self.previous().literal)
        if self.match([TokenType.LEFT_PAREN]):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Expr.Grouping(expr)
        raise self.error(self.peek(), "Expect expression")

    def consume(self, t, message):
        if (self.check(t)) : return self.advance()
        raise self.error(self.peek(), message)

    def error(self, token, message):
        self.error_handler.error(token, message)
        return ParseError()

    def synchronize(self):
        self.advance()
        while (not self.isAtEnd()):
            if (self.previous().type == TokenType.SEMICOLON) : return
            nextType = self.peek().type
            synchTypes = [  TokenType.CLASS, TokenType.FUN,
                        TokenType.VAR, TokenType.FOR,
                        TokenType.IF, TokenType.WHILE,
                        TokenType.PRINT, TokenType.RETURN]
            if nextType in synchTypes : return
            self.advance()

    def match(self, types):
        for t in types:
            if (self.check(t)):
                self.advance()
                return True
        return False

    def check(self,t):
        if (self.isAtEnd()) : return False
        return (self.peek().type == t)

    def advance(self):
        if (not (self.isAtEnd())) : self.current += 1
        return self.previous()

    def isAtEnd(self): return self.peek().type == TokenType.EOF

    def peek(self): return self.tokens[self.current]

    def previous(self): return self.tokens[self.current - 1]
