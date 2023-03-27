import Expr
import Stmt
from TokenType import TokenType
import ErrorHandler
from ErrorHandler import LoxRuntimeError, ErrorHandler
from Environment import Environment
import LoxCallable
from LoxCallable import LoxCallable
import NativeFunctions
from NativeFunctions import stringify
from LoxFunction import LoxFunction

class LoxTypeError(Exception):
    def __init__(self, token, message):
        self.token = token
        super().__init__(message)



class Interpreter(Expr.Visitor, Stmt.Visitor):
    def __init__(self):
        self.globalEnv = Environment()
        self.env = self.globalEnv
        for function, impl in NativeFunctions.NativeFunctionsList.items():
            self.globalEnv.define(function, impl())

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


    def visitVarStmt(self, stmt):
        value = None
        if stmt.initializer != None:
            value = self.evaluate(stmt.initializer)
        self.env.define(stmt.name.lexeme, value)
        return None

    def visitBlockStmt(self, stmt):
        self.executeBlock(stmt.statements, Environment(self.env))
        return None

    def visitIfStmt(self, stmt):

        if(self.isTruthy(self.evaluate(stmt.condition))):
            self.execute(stmt.thenBranch)
        elif(stmt.elseBranch):
            self.execute(stmt.elseBranch)
        return None

    def visitWhileStmt(self, stmt):
        while self.isTruthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
        return None


    def executeBlock(self, stmts, env):
        previous = self.env
        try:
            self.env = env
            for statement in stmts:
                self.execute(statement)
        finally:
            self.env = previous

    def visitFunctionStmt(self, stmt):
        function = LoxFunction(stmt)
        self.env.define(stmt.name.lexeme, function)
        return None



    """ Expressions """
    def visitCallExpr(self, expr):
        callee = self.evaluate(expr.callee)
        if (not isinstance(callee, LoxCallable)):
            raise LoxRuntimeError(expr.paren, "Can only call functions and classes.")
        arguments = [self.evaluate(argument) for argument in expr.arguments]
        function = callee

        if(len(arguments) != function.arity()):
            raise LoxRuntimeError(expr.paren, "Expected " + str(function.arity()) + " Arguments, but got " + str(len(arguments)) + ".")
        return function.call(self, arguments)

    def visitAssignExpr(self, expr):
        value = self.evaluate(expr.value)
        self.env.assign(expr.name, value)
        return value
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

    def isTruthy(self, obj):
        if (obj == None) : return False
        elif (isinstance(obj, bool)) : return obj
        return True

    def visitLogicalExpr(self,expr):
        left = self.evaluate(expr.left)
        if(expr.operator.type == TokenType.OR):
            if(self.isTruthy(left)): return left
        else:
            if(not self.isTruthy(left)): return left
        return self.evaluate(expr.right)

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
                return left + stringify(right)
            if (isinstance(right,str)):
                return stringify(left) + right
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
