class Visitor:
	def visitExpressionStmt(stmt):
		pass
	def visitPrintStmt(stmt):
		pass
	def visitVarStmt(stmt):
		pass
class Stmt:
	def accept(visitor):
		pass
class Expression(Stmt):
	def __init__(self, expression):
		self.expression= expression
	def accept(self, visitor):
		return visitor.visitExpressionStmt(self)
class Print(Stmt):
	def __init__(self, expression):
		self.expression= expression
	def accept(self, visitor):
		return visitor.visitPrintStmt(self)
class Var(Stmt):
	def __init__(self, name, initializer):
		self.name= name
		self.initializer= initializer
	def accept(self, visitor):
		return visitor.visitVarStmt(self)
class Visitor:
	def visitExpressionStmt(stmt):
		pass
	def visitPrintStmt(stmt):
		pass
	def visitVarStmt(stmt):
		pass
class Stmt:
	def accept(visitor):
		pass
class Expression(Stmt):
	def __init__(self, expression):
		self.expression= expression
	def accept(self, visitor):
		return visitor.visitExpressionStmt(self)
class Print(Stmt):
	def __init__(self, expression):
		self.expression= expression
	def accept(self, visitor):
		return visitor.visitPrintStmt(self)
class Var(Stmt):
	def __init__(self, name, initializer):
		self.name= name
		self.initializer= initializer
	def accept(self, visitor):
		return visitor.visitVarStmt(self)
