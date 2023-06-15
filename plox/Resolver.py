from enum import Enum
from enum import auto
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
from Return import Return
from Interpreter import Interpreter

class FunctionType(Enum):
    NONE = auto()
    FUNCTION = auto()

class Resolver(Expr.Visitor, Stmt.Visitor):
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.scopes = []
        self.currentFunction = FunctionType.NONE

    def visitBlockStmt(self, stmt):
        self.beginScope()
        self.resolveStmts(stmt.statements)
        self.endScope()
        return None

    def resolveStmts(self, stmts):
        for stmt in stmts:
            self.resolveStmt(stmt)

    def resolveStmt(self, stmt):
        stmt.accept(self)

    def resolveExpr(self, expr):
        expr.accept(self)

    def beginScope(self):
        self.scopes.append({})

    def endScope(self):
        self.scopes.pop()

    def visitVarStmt(self, stmt):
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolveExpr(stmt.initializer)
        self.define(stmt.name)
        return None

    def declare(self, token):
        if not self.scopes:
            return
        scope = self.scopes[-1]
        if token.lexeme in scope:
            ErrorHandler.TokenError(token, "Already have a variable with this name in this local scope.")
        scope[token.lexeme] = False

    def define(self, token):
        if not self.scopes:
            return
        self.scopes[-1][token.lexeme] = True

    def visitVariableExpr(self, expr):
        if self.scopes and self.scopes[-1].get(expr.name.lexeme, None)==False:
            ErrorHandler.TokenError(expr.name, "Can't reference local variable in it's own initializer")
        self.resolveLocal(expr, expr.name)

    def resolveLocal(self, expr, name):
        for i in range(len(self.scopes) - 1, -1, -1):
            if name.lexeme in self.scopes[i]:
                self.interpreter.resolve(expr, len(self.scopes) - i - 1)
                return

    def visitAssignExpr(self, expr):
        self.resolveExpr(expr.value)
        self.resolveLocal(expr, expr.name)

    def visitFunctionStmt(self, fn):
        self.declare(fn.name)
        self.define(fn.name)
        self.resolveFunction(fn, FunctionType.FUNCTION)
        return None

    def resolveFunction(self, fn, fnType):
        self.beginScope()
        enclosingFunction = self.currentFunction
        self.currentFunction = fnType
        for param in fn.params:
            self.declare(param)
            self.define(param)
        self.resolveStmts(fn.body)
        self.endScope()
        self.currentFunction = enclosingFunction

    def visitExpressionStmt(self, stmt):
        self.resolveExpr(stmt.expression)
        return None

    def visitIfStmt(self, stmt):
        self.resolveExpr(stmt.condition)
        self.resolveStmt(stmt.thenBranch)
        if stmt.elseBranch:
            self.resolveStmt(stmt.elseBranch)
        return None

    def visitReturnStmt(self,stmt):
        if self.currentFunction == FunctionType.NONE:
            ErrorHandler.TokenError(stmt.keyword, "Can't return from top level code")
        if stmt.value:
            self.resolveExpr(stmt.value)
        return None

    def visitWhileStmt(self,stmt):
        self.resolveExpr(stmt.condition)
        self.resolveStmt(stmt.body)
        return None

    def visitBinaryExpr(self, expr):
        self.resolveExpr(expr.left)
        self.resolveExpr(expr.right)
        return None

    def visitCallExpr(self,expr):
        self.resolveExpr(expr.callee)
        for arg in expr.arguments:
            self.resolveExpr(arg)
        return None

    def visitGroupingExpr(self,expr):
        self.resolve(expr.expression)
        return None

    def visitLiteralExpr(self,expr):
        return None

    def visitLogicalExpr(self,expr):
        self.resolve(expr.left)
        self.resolve(expr.right)
        return None

    def visitUnaryExpr(self, expr):
        self.resolve(expr.right)
        return None
