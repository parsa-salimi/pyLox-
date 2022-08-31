class Visitor:
	def visitBinaryExpr(expr):
		pass
	def visitGroupingExpr(expr):
		pass
	def visitLiteralExpr(expr):
		pass
	def visitUnaryExpr(expr):
		pass
class Expr:
	def accept(visitor):
		pass
class Binary(Expr):
	def __init__(self, left, operator, right):
		self.left= left
		self.operator= operator
		self.right= right
	def accept(self, visitor):
		return visitor.visitBinaryExpr(self)
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
class Unary(Expr):
	def __init__(self, operator, right):
		self.operator= operator
		self.right= right
	def accept(self, visitor):
		return visitor.visitUnaryExpr(self)
