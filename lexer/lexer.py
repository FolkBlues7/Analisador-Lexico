import ply.lex as lex
import sys
import os

# --- LÓGICA DE IMPORTAÇÃO COM FALLBACK ---
try:
    # 1. Tenta a importação relativa (CORRETO quando executado via main.py ou como módulo)
    from .tokens import tokens, reserved
except ImportError:
    # 2. Se falhar (ocorre quando executado DIRETAMENTE), tenta a importação absoluta.
    # É necessário adicionar o diretório pai ao path para encontrar 'tokens.py'
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from tokens import tokens, reserved
# --- FIM DA LÓGICA DE IMPORTAÇÃO ---

# =============================================================================
# REGRAS SIMPLES (t_...)
# =============================================================================

# Símbolos especiais:
t_LBRACE        = r'\{'
t_RBRACE        = r'\}'
t_LPAREN        = r'\('
t_RPAREN        = r'\)'
t_LBRACKET      = r'\['
t_RBRACKET      = r'\]'


# Outros Símbolos
t_DOTDOT        = r'\.\.'
t_ASTERISK      = r'\*'
t_AT            = r'@'
t_COLON         = r':'
t_COMMA         = r','

# Símbolos Compostos
t_ARROW_RL      = r'<>--'
t_ARROW_LR      = r'--<>'
t_DOUBLE_HYPHEN = r'--' #adicionado depois na nova versão do PDF


# Ignora espaços, tabs e comentários
t_ignore        = ' \t'
t_ignore_comment = r'//.*'

# =============================================================================
# REGRAS COM FUNÇÃO (t_...)
# =============================================================================

# GRUPO 1: Literais
def t_DATETIME_LITERAL(t):
    r"'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'"
    t.value = t.value[1:-1]
    return t

def t_DATE_LITERAL(t):
    r"'\d{4}-\d{2}-\d{2}'"
    t.value = t.value[1:-1]
    return t

def t_TIME_LITERAL(t):
    r"'\d{2}:\d{2}:\d{2}'"
    t.value = t.value[1:-1]
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\"]|\\.)*\"'
    t.value = t.value[1:-1]
    return t

# GRUPO 2: IDENTIFICADORES
def t_NEW_DATATYPE(t):
    r'[a-zA-Z]+DataType'
    return t

def t_INSTANCE_NAME(t):
    r'[a-zA-Z][a-zA-Z_]*[0-9]+'
    return t

def t_CLASS_NAME(t):
    r'[A-Z][a-zA-Z0-9_]*'
    return t

# Regra que captura Relações, Estereótipos e Palavras Reservadas
def t_RELATION_NAME(t):
    r'[a-z][a-zA-Z_\-]*'
    t.type = reserved.get(t.value, 'RELATION_NAME')
    return t

# GRUPO 3: CONTROLE E ERROS (Apenas as essenciais para o PLY)
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    # NOTA: Removida a chamada a find_column, pois ela foi retirada para simplificar.
    print(f"Erro Léxico: Caractere ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

# CRIAÇÃO DO OBJETO LEXER
lexer = lex.lex()

# FUNÇÃO AUXILIAR PARA RODAR O LEXER (REMOVIDA DE test_lexer.py)
def run_lexer_test(code_example, test_name):
    # Usa a mesma função de find_column que estava no seu código anterior se precisar de coluna,
    # caso contrário, basta usar a lógica do PLY. Vou mantê-lo simples aqui.
    
    output = []
    
    # Reseta o lexer
    lexer.input(code_example)
    
    # Processa os tokens
    while True:
        tok = lexer.token()
        if not tok:
            break
        # Formata a saída
        output.append(f"Tipo: {tok.type:<25} | Lexema: '{str(tok.value):<20}' | Linha: {tok.lineno}")
        
    return output