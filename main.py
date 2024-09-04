# features of TofuScript

#int, if, while, print


code = """
int a a = 5;
if (a > 0) {
    a = a + 1;
}
"""
from lexer import Lexer

l = Lexer(code)
l.lex()
for token in l.tokens:
    print(token)
minified_code = l.minify()
print(str(minified_code))
