class ASTNode:
    pass

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"NumberNode({self.value})"

class IdentifierNode(ASTNode):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"IdentifierNode({self.name})"

class BinaryOpNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"BinaryOpNode({self.left}, {self.operator}, {self.right})"

class AssignmentNode(ASTNode):
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

    def __repr__(self):
        return f"AssignmentNode({self.identifier}, {self.value})"

class IfNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"IfNode({self.condition}, {self.body})"

class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"WhileNode({self.condition}, {self.body})"

class PrintNode(ASTNode):
    def __init__(self, value):
        self.value = value
