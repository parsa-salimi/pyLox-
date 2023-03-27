class Visitor:
	def visitBlockStmt(stmt):
		pass
	def visitExpressionStmt(stmt):
		pass
	def visitIfStmt(stmt):
		pass
	def visitFunctionStmt(stmt):
		pass
	def visitReturnStmt(stmt):
		pass
	def visitVarStmt(stmt):
		pass
	def visitWhileStmt(stmt):
		pass
class Stmt:
	def accept(visitor):
		pass
class Block(Stmt):
	def __init__(self, statements):
		self.statements= statements
	def accept(self, visitor):
		return visitor.visitBlockStmt(self)
class Expression(Stmt):
	def __init__(self, expression):
		self.expression= expression
	def accept(self, visitor):
		return visitor.visitExpressionStmt(self)
class If(Stmt):
	def __init__(self, condition, thenBranch, elseBranch):
		self.condition= condition
		self.thenBranch= thenBranch
		self.elseBranch= elseBranch
	def accept(self, visitor):
		return visitor.visitIfStmt(self)
class Function(Stmt):
	def __init__(self, name, params, body):
		self.name= name
		self.params= params
		self.body= body
	def accept(self, visitor):
		return visitor.visitFunctionStmt(self)
class Return(Stmt):
	def __init__(self, keyword, value):
		self.keyword= keyword
		self.value= value
	def accept(self, visitor):
		return visitor.visitReturnStmt(self)
class Var(Stmt):
	def __init__(self, name, initializer):
		self.name= name
		self.initializer= initializer
	def accept(self, visitor):
		return visitor.visitVarStmt(self)
class While(Stmt):
	def __init__(self, condition, body):
		self.condition= condition
		self.body= body
	def accept(self, visitor):
		return visitor.visitWhileStmt(self)
