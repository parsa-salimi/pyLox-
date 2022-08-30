Class Visitor:
	def visitBinaryExpr(expr):
		pass
	def visitGroupingExpr(expr):
		pass
	def visitLiteralExpr(expr):
		pass
	def visitUnaryExpr(expr):
		pass
class Expr:
	def accpet(visitor):
		pass
class Binary(Expr):
	def __init__(self, left, operator, right):
		self.left= left
		self.operator= operator
		self.right= right
	def accept(visitor):
		return visitor.visitBinaryExpr()
class Grouping(Expr):
	def __init__(self, expression):
		self.expression= expression
	def accept(visitor):
		return visitor.visitGroupingExpr()
class Literal(Expr):
	def __init__(self, value):
		self.value= value
	def accept(visitor):
		return visitor.visitLiteralExpr()
class Unary(Expr):
	def __init__(self, operator, right):
		self.operator= operator
		self.right= right
	def accept(visitor):
		return visitor.visitUnaryExpr()
