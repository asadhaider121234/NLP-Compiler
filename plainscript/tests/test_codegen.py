import pytest
from plainscript.compiler.lexer import Lexer
from plainscript.compiler.parser import Parser
from plainscript.compiler.codegen import CodeGenerator

def test_codegen_basic():
    code = 'set x to 10 plus 5'
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens, code)
    ast = parser.parse()
    generator = CodeGenerator()
    py_code = generator.generate(ast)
    assert 'x = (10 + 5)' in py_code

def test_codegen_joined():
    code = 'show "hi" joined with " there"'
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens, code)
    ast = parser.parse()
    generator = CodeGenerator()
    py_code = generator.generate(ast)
    assert 'print((str("hi") + str(" there")))' in py_code
    
def test_codegen_repeat():
    code = "repeat 3 times\n    show 1\nend"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens, code)
    ast = parser.parse()
    generator = CodeGenerator()
    py_code = generator.generate(ast)
    assert 'for _i1 in range(3):' in py_code
    assert '    print(1)' in py_code
