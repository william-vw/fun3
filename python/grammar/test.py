from antlr4 import *
from parser.n3Lexer import n3Lexer
from parser.n3Parser import n3Parser

input_text =  ":will :is :cool ." #input("> ")
lexer = n3Lexer(InputStream(input_text))
stream = CommonTokenStream(lexer)
parser = n3Parser(stream)

tree = parser.n3Doc()

print(tree.toStringTree(recog=parser))