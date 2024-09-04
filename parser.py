# constructs supported by the language:
# Variable declaration: int a = 5;
# Assignment: a = 10;
# arithmetic Expression: a + b * c / d 
# conditional: if (a > 0) { ... }
# while loop: while (a > 0) { ... }

#first thing to add will be another keyword for assignment (like var or let)
#second thing to add will be const/immutable variables by default

"""
program        ::= statement_list
statement_list ::= statement ";" | statement_list statement ";"
statement      ::= declaration | assignment | if_statement | while_statement
declaration    ::= "int" IDENTIFIER "=" expression
assignment     ::= IDENTIFIER "=" expression
if_statement   ::= "if" "(" expression ")" statement
expression     ::= term | expression "+" term | expression "-" term
term           ::= factor | term "*" factor | term "/" factor
factor         ::= NUMBER | IDENTIFIER | "(" expression ")"
"""

from ast_nodes import *

from token_types import TOKEN_TYPES
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def advance(self):
        self.position += 1

    def expect(self, token_type):
        token = self.current_token()
        if token and token.type == token_type:
            self.advance()
            return token  
        else:
            raise SyntaxError(f"Expected {token_type}, but got {token.type if token else 'EOF'}")

    def parse(self):
        return self.parse_statement_list()

    def parse_statement_list(self):
        statements = []
        while self.current_token() and self.current_token().type != TOKEN_TYPES['BRACE']:
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        token = self.current_token()
        if token.type == TOKEN_TYPES['TYPE'] and token.value == 'int': #NOTE I don't actually think  we need to specify INT as 'TYPES' is all 'declarables' 
            return self.parse_declaration()
        elif token.type == TOKEN_TYPES['IDENTIFIER']:
            return self.parse_assignment()
        elif token.type == TOKEN_TYPES['KEYWORD'] and token.value == 'if':
            return self.parse_if_statement()
        elif token.type == TOKEN_TYPES['KEYWORD'] and token.value == 'print':
            return self.parse_print_statement()
        else:
            raise SyntaxError(f"Unexpected statement starting with {token}")
        
    def parse_assignment(self):
        identifier = self.expect(TOKEN_TYPES['IDENTIFIER'])
        self.expect(TOKEN_TYPES['ASSIGN'])
        value = self.parse_expression()
        self.expect(TOKEN_TYPES['SEMICOLON'])
        return AssignmentNode(identifier=identifier.value, value=value)

    def parse_declaration(self):
        self.expect(TOKEN_TYPES['TYPE']) #int is currently the only excepted declaration type
        identifier = self.expect(TOKEN_TYPES['IDENTIFIER'])
        self.expect(TOKEN_TYPES['ASSIGN'])
        value = self.parse_expression() #parse the right hand of the operator
        self.expect(TOKEN_TYPES['SEMICOLON'])
        return AssignmentNode(identifier=identifier.value, value=value)

    def parse_expression(self):
        left = self.parse_term()
        token = self.current_token()
        while token and token.type == TOKEN_TYPES['OPERATOR']:
            operator = token.value
            self.advance()
            right = self.parse_term()
            left = BinaryOpNode(left=left, operator=operator, right=right)
            token = self.current_token()
        return left


    def parse_term(self):
        token = self.current_token()

        if token.type == TOKEN_TYPES['NUMBER']:
            self.advance()
            return NumberNode(token.value)
        
        elif token.type == TOKEN_TYPES['IDENTIFIER']:
            self.advance()
            return IdentifierNode(token.value)

        #TODO this is naive as it doesn't differentiate between open and close parens, the same behavior happens for the brace as well
        elif token.type == TOKEN_TYPES['PAREN']:
            self.expect(TOKEN_TYPES['PAREN'])
            expression = self.parse_expression()
            self.expect(TOKEN_TYPES['PAREN'])
            return expression

        else:
            raise SyntaxError(f"unexpected token {token}")

    def parse_if_statement(self):
        self.expect(TOKEN_TYPES['KEYWORD']) #TODO check specific keywords
        self.expect(TOKEN_TYPES['PAREN'])

        condition = self.parse_expression()

        self.expect(TOKEN_TYPES['PAREN'])

        self.expect(TOKEN_TYPES['BRACE'])
        body = self.parse_statement_list()
        self.expect(TOKEN_TYPES['BRACE'])

        return IfNode(condition=condition, body=body)

    #TODO: create separate tokens for open and close parens and braces.
    def parse_print_statement(self):
        self.expect(TOKEN_TYPES['KEYWORD'])
        self.expect(TOKEN_TYPES['PAREN'])
        value = self.parse_expression()
        self.expect(TOKEN_TYPES['PAREN'])
        self.expect(TOKEN_TYPES['SEMICOLON'])
        return PrintNode(value)