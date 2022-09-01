import Expr
from TokenType import TokenType

class LoxTypeError(Exception):
    def __init__(self, token, message):
        self.token = token
        super().__init__(message)

class Interpreter(Expr.Visitor):
    def __init__(self, ErrorHandler):
        self.error_handler = ErrorHandler
    def interpret(self,expression):
        try:
            value = self.evaluate(expression)
            print(self.stringify(value))
        except LoxTypeError as err:
            return self.error_handler.runtimeError(err)


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
        raise LoxTypeError(operator, "Operand must be a number")

    def checkNumberOperands(self, operator, left, right):
        if (isinstance(left, float) and isinstance(right,float)): return
        raise LoxTypeError(operator, "Operands must be numbers")

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
                raise LoxTypeError(expr.operator, "division by zero")
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
            raise LoxTypeError(operator, "operands must be numbers or strings")
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

        

    def evaluate(self, expr): return expr.accept(self)

    def stringify(self, obj):
        if (obj == None) : return "nil"
        if (isinstance(obj,float)):
            text = str(obj)
            if (text.endswith(".0")) : text = text[0: len(text) - 2]
            return text
        return str(obj)