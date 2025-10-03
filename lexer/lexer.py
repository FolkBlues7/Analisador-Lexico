import ply.lex as lex
from lexer.tokens import tokens

class Lexer:
    def __init__(self):
        self.lexer = lex.lex(module=self)

    # Regras para tokens básicos (exemplo inicial)
    t_ignore = ' \t\n'

    # Símbolos especiais
    t_LBRACE   = r'\{'
    t_RBRACE   = r'\}'
    t_LPAREN   = r'\('
    t_RPAREN   = r'\)'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_COMMA    = r','

    # Palavras reservadas
    reserved = {
        'genset' : 'GENSET',
        'disjoint' : 'DISJOINT',
        'complete' : 'COMPLETE',
        'general' : 'GENERAL',
        'specifics' : 'SPECIFICS',
        'where' : 'WHERE',
        'package' : 'PACKAGE',
    }

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'ID')  # Se não for palavra reservada, é identificador
        return t

    def t_error(self, t):
        print(f"Erro léxico: caractere inesperado '{t.value[0]}' na posição {t.lexpos}")
        t.lexer.skip(1)

    def tokenize(self, data):
        self.lexer.input(data)
        return [tok for tok in self.lexer]
