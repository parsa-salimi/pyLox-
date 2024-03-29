class Visitor:
	def visitAssignExpr(expr):
		pass
	def visitBinaryExpr(expr):
		pass
	def visitCallExpr(expr):
		pass
	def visitGroupingExpr(expr):
		pass
	def visitLiteralExpr(expr):
		pass
	def visitLogicalExpr(expr):
		pass
	def visitUnaryExpr(expr):
		pass
	def visitVariableExpr(expr):
		pass
class Expr:
	def accept(visitor):
		pass
class Assign(Expr):
	def __init__(self, name, value):
		self.name= name
		self.value= value
	def accept(self, visitor):
		return visitor.visitAssignExpr(self)
class Binary(Expr):
	def __init__(self, left, operator, right):
		self.left= left
		self.operator= operator
		self.right= right
	def accept(self, visitor):
		return visitor.visitBinaryExpr(self)
class Call(Expr):
	def __init__(self, callee, paren, arguments):
		self.callee= callee
		self.paren= paren
		self.arguments= arguments
	def accept(self, visitor):
		return visitor.visitCallExpr(self)
class Grouping(Expr):
	def __init__(self, expression):
		self.expression= expression
	def accept(self, visitor):
		return visitor.visitGroupingExpr(self)
class Literal(Expr):
	def __init__(self, value):
		self.value= value
	def accept(self, visitor):
		return visitor.visitLiteralExpr(self)
class Logical(Expr):
	def __init__(self, left, operator, right):
		self.left= left
		self.operator= operator
		self.right= right
	def accept(self, visitor):
		return visitor.visitLogicalExpr(self)
class Unary(Expr):
	def __init__(self, operator, right):
		self.operator= operator
		self.right= right
	def accept(self, visitor):
		return visitor.visitUnaryExpr(self)
class Variable(Expr):
	def __init__(self, name):
		self.name= name
	def accept(self, visitor):
		return visitor.visitVariableExpr(self)
