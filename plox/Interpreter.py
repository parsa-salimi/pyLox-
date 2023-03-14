import Expr
import Stmt
from TokenType import TokenType
import ErrorHandler
from ErrorHandler import LoxRuntimeError, ErrorHandler
from Environment import Environment

class LoxTypeError(Exception):
    def __init__(self, token, message):
        self.token = token
        super().__init__(message)

class Interpreter(Expr.Visitor, Stmt.Visitor):
    def __init__(self):
        self.env = Environment()

    def interpret(self,listStmts):
        try:
            for statement in listStmts:
                self.execute(statement)
        except LoxRuntimeError as err:
            return ErrorHandler.runtimeError(err)

    """Statements"""
    def visitExpressionStmt(self, stmt):
        self.evaluate(stmt.expression)
        return None

    def visitPrintStmt(self, stmt):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None

    def visitVarStmt(self, stmt):
        value = None
        if stmt.initializer != None:
            value = self.evaluate(stmt.initializer)
        self.env.define(stmt.name.lexeme, value)
        return None

    """ Expressions """
    def visitVariableExpr(self, expr): return self.env.get(expr.name)
    def visitLiteralExpr(self, expr): return expr.value
    def visitGroupingExpr(self, expr) : return self.evaluate(expr.expression)
    def visitUnaryExpr(self, expr):
        right = self.evaluate(expr.right)
        if (expr.operator.type == TokenType.MINUS):
            self.checkNumberOperand(expr.operator, right)
            return -right
        elif (expr.operator.type == TokenType.BANG): return (not self.isTruthy(right))
        return None

    def checkNumberOperand(self, operator, operand):
        if isinstance(operator, float) : return
        raise LoxRuntimeError(operator, "Operand must be a number")

    def checkNumberOperands(self, operator, left, right):
        if (isinstance(left, float) and isinstance(right,float)): return
        raise LoxRuntimeError(operator, "Operands must be numbers")

    def isTruthy(self, object):
        if (object == None) : return False
        elif (isinstance(object, bool)) : return object
        return True

    def visitBinaryExpr(self,expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if(expr.operator.type == TokenType.MINUS):
            self.checkNumberOperands(expr.operator, left, right)
            return left - right
        elif(expr.operator.type == TokenType.SLASH):
            self.checkNumberOperands(expr.operator, left, right)
            if (right == 0):
                raise LoxRuntimeError(expr.operator, "division by zero")
            return left / right
        elif(expr.operator.type == TokenType.STAR):
            self.checkNumberOperands(expr.operator, left, right)
            return left * right
        elif(expr.operator.type == TokenType.PLUS) :
            if (isinstance(left, str) and isinstance(right,str)):
                return left + right
            if (isinstance(left, float) and isinstance(right, float)):
                return left + right
            if (isinstance(left,str)):
                return left + self.stringify(right)
            if (isinstance(right,str)):
                return self.stringify(left) + right
            return left + right
            raise LoxRuntimeError(operator, "operands must be numbers or strings")
        elif(expr.operator.type == TokenType.GREATER) :
            self.checkNumberOperands(expr.operator, left, right)
            return left > right
        elif(expr.operator.type == TokenType.GREATER_EQUAL) :
            self.checkNumberOperands(expr.operator, left, right)
            return left >= right
        elif(expr.operator.type == TokenType.LESS) :
            self.checkNumberOperands(expr.operator, left, right)
            return left < right
        elif(expr.operator.type == TokenType.LESS_EQUAL) :
            self.checkNumberOperands(expr.operator, left, right)
            return left <= right
        elif(expr.operator.type == TokenType.BANG_EQUAL) : return left != right
        elif(expr.operator.type == TokenType.EQUAL_EQUAL) : return left == right



    """ Helpers"""
    def execute(self, stmt): return stmt.accept(self)

    def evaluate(self, expr): return expr.accept(self)

    def stringify(self, obj):
        if (obj == None) : return "nil"
        if (isinstance(obj,float)):
            text = str(obj)
            if (text.endswith(".0")) : text = text[0: len(text) - 2]
            return text
        return str(obj)