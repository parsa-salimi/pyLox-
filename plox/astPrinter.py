import Expr
from TokenType import TokenType
from Token import Token


class AstPrinter(Expr.Visitor):
    def print(self, expr):
        return expr.accept(self)
    
    def visitBinaryExpr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitGroupingExpr(self, expr):
        return self.parenthesize("group", expr.expression)

    def visitLiteralExpr(self, expr):
        if (expr.value == None) : return None
        else : return str(expr.value)

    def visitUnaryExpr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name, *exprs):
        builder = "(" + name
        for expr in exprs:
            builder += " " + expr.accept(self)
        builder += ")"
        return builder







