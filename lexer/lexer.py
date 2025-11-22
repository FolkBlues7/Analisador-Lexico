import ply.lex as lex
import sys
import os

# --- LÓGICA DE IMPORTAÇÃO COM FALLBACK ---
try:
    # 1. Tenta a importação relativa (CORRETO quando executado via main.py ou como módulo)
    from .tokens import tokens, reserved
except ImportError:
    # 2. Se falhar, tenta a importação absoluta.
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
t_DOUBLE_HYPHEN = r'--'

# Ignora espaços, tabs e comentários
t_ignore        = ' \t'
t_ignore_comment = r'//.*'

# =============================================================================
# REGRAS COM FUNÇÃO (t_...)
# =============================================================================

# GRUPO 1: Literais (Mantidos conforme seu original)
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
    r"\'([^\\\']|\\.)*\'"  # Ajustei para aspas simples pois os exemplos usam 'string'
    t.value = t.value[1:-1]
    return t

# GRUPO 2: IDENTIFICADORES (Lógica Unificada para corrigir Criterion_A1a)
# Substitui t_NEW_DATATYPE, t_INSTANCE_NAME, t_CLASS_NAME e t_RELATION_NAME
# por uma única regra robusta.
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_\-]*'
    
    # 1. Verifica se é Palavra Reservada (kind, package, specializes, etc.)
    reserved_type = reserved.get(t.value)
    if reserved_type:
        t.type = reserved_type
        return t

    # 2. Verifica se é um Novo Tipo de Dado (termina com 'DataType')
    if t.value.endswith('DataType'):
        t.type = 'NEW_DATATYPE'
        return t

    # 3. Verifica se é Nome de Instância (termina com número)
    # Ex: Criterion_A1 (cai aqui). 
    # Criterion_A1a (NÃO cai aqui, pois termina com 'a').
    if t.value[-1].isdigit():
        t.type = 'INSTANCE_NAME'
        return t
        
    # 4. Verifica se é Nome de Relação (começa com minúscula e não é reservada)
    if t.value[0].islower():
        t.type = 'RELATION_NAME'
        return t

    # 5. Se não for nada acima, é um Nome de Classe Padrão (começa com maiúscula)
    # Ex: Person, Criterion_A1a, Blue
    t.type = 'CLASS_NAME'
    return t

# GRUPO 3: CONTROLE E ERROS
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Erro Léxico: Caractere ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

# CRIAÇÃO DO OBJETO LEXER
lexer = lex.lex()

# FUNÇÃO AUXILIAR PARA RODAR O LEXER (RESTAURADA)
def run_lexer_test(code_example, test_name):
    output = []
    
    # Reseta o lexer
    lexer.lineno = 1
    lexer.input(code_example)
    
    # Processa os tokens
    while True:
        tok = lexer.token()
        if not tok:
            break
        # Formata a saída
        output.append(f"Tipo: {tok.type:<25} | Lexema: '{str(tok.value):<20}' | Linha: {tok.lineno}")
        
    return output