import re

from token_types import TOKEN_TYPES
KEYWORDS = ['if', 'while', 'return', 'print']
TYPES = ['int']


class Token:
    def __init__(self, token_type, value, filename, line, column):
        self.type = token_type
        self.value = value
        self.filename = filename
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, {repr(self.filename)},line: {self.line},{self.column})"

class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.tokens = []

    def lex(self):
        while self.position < len(self.code):
            
            current_char = self.code[self.position]

            if current_char.isspace() or current_char == '\\n':
                self.position += 1 # whitespace is ignored
            elif current_char.isdigit():
                self.tokens.append(self.consume_number())
            elif current_char.isalpha() or current_char == '_':
                self.tokens.append(self.consume_identifier_or_keyword())
            elif current_char == '=':
                if self.position + 1 < len(self.code) and self.code[self.position + 1] == '=':
                    self.tokens.append(Token(TOKEN_TYPES['OPERATOR'], '==', '', 0, 0))
                    self.position += 2
                else:
                    self.tokens.append(Token(TOKEN_TYPES['ASSIGN'], '=', '', 0, 0))
                    self.position += 1
            elif current_char in '+-*/><!':
                self.tokens.append(self.consume_operator())
            elif current_char == ';':
                self.tokens.append(Token(TOKEN_TYPES['SEMICOLON'], ';', '', 0, 0))
                self.position += 1
            elif current_char in '{}':
                self.tokens.append(self.consume_brace())
            elif current_char in '()':
                self.tokens.append(self.consume_paren())
            else:
                self.tokens.append(self.consume_unknown())
        return self.tokens

    def consume_number(self):
        start = self.position
        while self.position < len(self.code) and self.code[self.position].isdigit():
            self.position += 1
        return Token(TOKEN_TYPES['NUMBER'], int(self.code[start:self.position]), '', 0,0)

    def consume_identifier_or_keyword(self):
        start = self.position
        while self.position < len(self.code) and (self.code[self.position].isalnum() or self.code[self.position] == '_'):
            self.position += 1
        value = self.code[start:self.position]
        if value in KEYWORDS:
            return Token(TOKEN_TYPES['KEYWORD'], value, '', 0, 0)
        elif value in TYPES:
            return Token(TOKEN_TYPES['TYPE'], value, '', 0, 0)
        else:
            return Token(TOKEN_TYPES['IDENTIFIER'], value, '', 0, 0)
    
    def consume_operator(self):
        start = self.position
        if self.position + 1 < len(self.code) and self.code[self.position:self.position+2] in ['==', '!=', '>=', '<=']:
            self.position += 2
            return Token(TOKEN_TYPES['OPERATOR'], self.code[start:self.position], '', 0, 0)
        else:
            self.position += 1
            return Token(TOKEN_TYPES['OPERATOR'], self.code[start:self.position], '', 0, 0)

    def consume_brace(self):
        current_char = self.code[self.position]
        self.position += 1
        return Token(TOKEN_TYPES['BRACE'], current_char, '', 0, 0)

    def consume_paren(self):
        current_char = self.code[self.position]
        self.position += 1
        return Token(TOKEN_TYPES['PAREN'], current_char, '', 0, 0)

    def consume_unknown(self):
        self.position += 1
        return Token(TOKEN_TYPES['UNKNOWN'], self.code[self.position], '', 0,0)



    def minify(self):
        token_values = ""
        for token in self.tokens:
            token_values += str(token.value)
        return token_values