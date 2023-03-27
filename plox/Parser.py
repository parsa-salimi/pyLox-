from TokenType import TokenType
import Expr
import Stmt
import ErrorHandler
from ErrorHandler import LoxRuntimeError, ErrorHandler

class ParseError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.statements = []
        #self.error_handler = error_handler

    def parse(self):
        while(not (self.isAtEnd())):
            self.statements.append(self.declaration())
        return self.statements

    def declaration(self):
        try:
            if(self.match([TokenType.FUN])): return self.function("function")
            if(self.match([TokenType.VAR])):
                return self.varDeclaration()
            else: return self.statement()
        except ParseError:
            self.synchronize()
            return None

    def function(self, kind):
        name = self.consume(TokenType.IDENTIFIER, "Expect " + kind + " name.")
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after " + kind + " name.")
        parameters = []
        if(not self.check(TokenType.RIGHT_PAREN)):
            condition = True
            while condition:
                if len(parameters) >= 255:
                    self.error(self.peek(), "Can't have more than 255 params.")
                parameters.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name"))
                condition = self.match([TokenType.COMMA])
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after " + kind + "params.")
        self.consume(TokenType.LEFT_BRACE, "Expect '{' before " + kind + "body.")
        body = self.block()
        return Stmt.Function(name, parameters, body)

    def varDeclaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name")
        value = None
        if(self.match([TokenType.EQUAL])):
            value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ; after initialization expression")
        return Stmt.Var(name, value)

    def statement(self):
        if(self.match([TokenType.IF])):
            return self.ifStatement()
        if(self.match([TokenType.WHILE])):
            return self.whileStatement()
        if(self.match([TokenType.FOR])):
            return self.forStatement()
        if(self.match([TokenType.LEFT_BRACE])):
            return Stmt.Block(self.block())
        else: return self.expressionStatement()

    def ifStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect ( after If.")
        ifExpression = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ) after If condition.")
        thenBranch = self.statement()
        elseBranch = None
        if(self.match([TokenType.ELSE])):
            elseBranch = self.statement()
        return Stmt.If(ifExpression, thenBranch, elseBranch)

    def whileStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect ( after While.")
        expr = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ) after While condition.")
        body = self.statement()
        return Stmt.While(expr, body)

    def forStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect ( after For.")
        initializer = None
        if(self.match([TokenType.SEMICOLON])):
            initializer = None
        elif(self.match([TokenType.VAR])):
            initializer = self.varDeclaration()
        else:
            initializer = self.expressionStatement()
        condition = None
        if(not self.check([TokenType.SEMICOLON])):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ; after for loop condition")
        increment = None
        if(not self.check([TokenType.RIGHT_PAREN])):
            increment = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ) after for loop increment")

        body = self.statement()
        if increment:
            body = Stmt.Block([body, increment])
        if (not condition): condition = Expr.Literal(True)
        body = Stmt.While(condition, body)
        if initializer:
            body = Stmt.Block([initializer, body])
        return body

    def block(self):
        stmts = []
        while (not self.check(TokenType.RIGHT_BRACE)) and (not self.isAtEnd()):
            stmts.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, "Expect } after block")
        return stmts


    def expressionStatement(self):
        value=self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ; after expression")
        return Stmt.Expression(value)

    def expression(self): return self.assignment()

    def assignment(self):
        expr = self.orExpr()
        if(self.match([TokenType.EQUAL])):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, Expr.Variable):
                name = expr.name
                return Expr.Assign(name, value)
            self.error(equals, "Invalid assignment target.")
        return expr

    def orExpr(self):
        expr = self.andExpr()
        while(self.match([TokenType.OR])):
            operator = self.previous()
            right = self.andExpr()
            expr = Expr.Logical(expr, operator, right)
        return expr

    def andExpr(self):
        expr = self.equality()
        while(self.match([TokenType.AND])):
            operator = self.previous()
            right = self.equality()
            expr = Expr.Logical(expr, operator, right)
        return expr

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
        return self.call()

    def call(self):
        expr = self.primary()

        while True:

            if(self.match([TokenType.LEFT_PAREN])):
                expr = self.finishCall(expr)
            else:
                break
        return expr

    def finishCall(self, callee):
        args = []
        condition = True
        if (not self.check(TokenType.RIGHT_PAREN)):
            while condition:
                args.append(self.expression())
                condition =  self.match([TokenType.COMMA])
        if(len(args) >= 255):
            self.error(self.peek(), "Can't have more than 255 arguments")
        paren = self.consume(TokenType.RIGHT_PAREN, "Expected ) after arguments to function call")
        return Expr.Call(callee, paren, args)




    def primary(self):
        if self.match([TokenType.FALSE]) : return Expr.Literal(False)
        if self.match([TokenType.TRUE]) : return Expr.Literal(True)
        if self.match([TokenType.NIL]) : return Expr.Literal(None)
        if self.match([TokenType.NUMBER, TokenType.STRING]): return Expr.Literal(self.previous().literal)
        if self.match([TokenType.IDENTIFIER]): return Expr.Variable(self.previous())
        if self.match([TokenType.LEFT_PAREN]):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Expr.Grouping(expr)
        raise self.error(self.peek(), "Expect expression")

    def consume(self, t, message):
        if (self.check(t)) : return self.advance()
        raise self.error(self.peek(), message)

    def error(self, token, message):
        ErrorHandler.TokenError(token, message)
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
