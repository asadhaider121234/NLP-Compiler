# ============================================
#   LISP Lexical Analyzer (Lexer) in Python
# ============================================

import re

# ─────────────────────────────────────────
#  Token Types
# ─────────────────────────────────────────
TOKEN_TYPES = {
    'LPAREN'  : r'\(',
    'RPAREN'  : r'\)',
    'INTEGER' : r'-?\d+',
    'FLOAT'   : r'-?\d+\.\d+',
    'STRING'  : r'"[^"]*"',
    'BOOLEAN' : r'#t|#f',
    'SYMBOL'  : r'[a-zA-Z_+\-*/=<>!?][a-zA-Z0-9_+\-*/=<>!?]*',
    'WHITESPACE': r'[ \t\n]+',
    'COMMENT' : r';[^\n]*',
}

# ─────────────────────────────────────────
#  Token Class
# ─────────────────────────────────────────
class Token:
    def __init__(self, type_, value, line):
        self.type  = type_
        self.value = value
        self.line  = line

    def __repr__(self):
        return f'Token({self.type:10} | value: {self.value!r:20} | line: {self.line})'


# ─────────────────────────────────────────
#  Lexer Class
# ─────────────────────────────────────────
class Lexer:
    def __init__(self, source_code):
        self.source = source_code
        self.tokens = []
        self.line   = 1

    def tokenize(self):
        source = self.source
        pos    = 0

        # Build a combined master regex pattern (order matters!)
        # FLOAT must come before INTEGER to avoid partial matches
        master_pattern = '|'.join(
            f'(?P<{name}>{pattern})'
            for name, pattern in [
                ('COMMENT'    , TOKEN_TYPES['COMMENT']),
                ('FLOAT'      , TOKEN_TYPES['FLOAT']),
                ('INTEGER'    , TOKEN_TYPES['INTEGER']),
                ('STRING'     , TOKEN_TYPES['STRING']),
                ('BOOLEAN'    , TOKEN_TYPES['BOOLEAN']),
                ('LPAREN'     , TOKEN_TYPES['LPAREN']),
                ('RPAREN'     , TOKEN_TYPES['RPAREN']),
                ('SYMBOL'     , TOKEN_TYPES['SYMBOL']),
                ('WHITESPACE' , TOKEN_TYPES['WHITESPACE']),
            ]
        )

        regex = re.compile(master_pattern)

        for match in regex.finditer(source):
            token_type = match.lastgroup
            value      = match.group()

            # Count lines
            if '\n' in value:
                self.line += value.count('\n')

            # Skip whitespace and comments
            if token_type in ('WHITESPACE', 'COMMENT'):
                continue

            # Convert values to proper Python types
            if token_type == 'INTEGER':
                value = int(value)
            elif token_type == 'FLOAT':
                value = float(value)
            elif token_type == 'BOOLEAN':
                value = True if value == '#t' else False
            elif token_type == 'STRING':
                value = value[1:-1]  # strip the quotes

            token = Token(token_type, value, self.line)
            self.tokens.append(token)

        return self.tokens


# ─────────────────────────────────────────
#  Error Detection
# ─────────────────────────────────────────
def check_errors(source):
    # Check for unmatched parentheses
    open_count  = source.count('(')
    close_count = source.count(')')
    if open_count != close_count:
        print(f"⚠️  Warning: Unmatched parentheses! '(' count={open_count}, ')' count={close_count}")

    # Check for unclosed strings
    if source.count('"') % 2 != 0:
        print("⚠️  Warning: Unclosed string literal detected!")


# ─────────────────────────────────────────
#  Main - Test the Lexer
# ─────────────────────────────────────────
if __name__ == '__main__':

    # Sample LISP source code
    source_code = """
    ; This is a comment
    (define x 42)
    (define pi 3.14)
    (define name "Alice")
    (define flag #t)

    (define (square n)
        (* n n))

    (if (> x 10)
        (display "x is greater than 10")
        (display "x is small"))

    (+ 1 2 3 4 5)
    """

    print("=" * 55)
    print("         LISP LEXICAL ANALYZER OUTPUT")
    print("=" * 55)

    # Check for basic errors
    check_errors(source_code)

    # Run the lexer
    lexer  = Lexer(source_code)
    tokens = lexer.tokenize()

    # Print all tokens
    for token in tokens:
        print(token)

    print("=" * 55)
    print(f"  Total Tokens Found: {len(tokens)}")
    print("=" * 55)