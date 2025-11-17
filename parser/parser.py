import ply.yacc as yacc
import json

# =============================================================================
# 1. IMPORTAÇÃO DOS TOKENS E LEXER
# =============================================================================
try:
    # Ajuste o caminho de importação conforme a estrutura real do seu projeto
    from lexer.lexer import tokens, lexer
except ImportError:
    print(
        "[ERRO FATAL] Não foi possível importar a lista de tokens do seu lexer. Por favor, verifique o caminho."
    )
    exit(1)

# =============================================================================
# 2. REGRAS DE GRAMÁTICA (TONTO)
# =============================================================================

# ----------------------------------
# A. REGRA PRINCIPAL (RAIZ DA ÁRVORE)
# ----------------------------------
def p_programa(p):
    """programa : declaracao_package declaracoes_pos_package"""
    
    # p[1] é a ÚNICA declaração de Package
    # p[2] são as outras declarações (Classes, Relações, etc.)

    # Constrói o nó raiz da AST
    p[0] = {
        "type": "OntologyModel",
        "package": p[1],
        "declarations": p[2],
    }

# ----------------------------------
# B. DECLARAÇÃO DE PACOTE
# ----------------------------------
def p_declaracao_package(p):
    """declaracao_package : PACKAGE CLASS_NAME"""
    p[0] = {"type": "Package", "name": p[2]}


# ----------------------------------
# C. LISTA DE DECLARAÇÕES PÓS-PACOTE
# ----------------------------------
def p_declaracoes_pos_package(p):
    """declaracoes_pos_package : declaracao declaracoes_pos_package
                               | empty"""
    # Esta é uma regra de lista recursiva.
    # p[1] é a declaração atual (ex: uma classe)
    # p[2] é a lista do resto das declarações
    if len(p) == 3:
        p[0] = [p[1]] + p[2]  # Adiciona a declaração atual à lista
    else:
        p[0] = [] # Caso 'empty' (lista vazia)

# ----------------------------------
# D. HUB DE DECLARAÇÕES
# ----------------------------------
def p_declaracao(p):
    """declaracao : declaracao_classe
                   | declaracao_enum""" # <-- (NOVO) Adicionado enum ao hub
    # Este é o "hub".
    # No futuro, adicionaremos:
    #            | declaracao_genset
    #            | ...
    p[0] = p[1]

# ----------------------------------
# E. DECLARAÇÃO DE CLASSE (CONSTRUTO 2)
# ----------------------------------
def p_declaracao_classe(p):
    """declaracao_classe : estereotipo_classe CLASS_NAME classe_specialization classe_body"""
    p[0] = {
        "type": "ClassDeclaration",
        "stereotype": p[1],
        "name": p[2],
        "specializes": p[3], 
        "body": p[4]         
    }

def p_classe_specialization(p):
    """classe_specialization : SPECIALIZES lista_nomes_classe
                             | empty"""
    if len(p) == 3:
        p[0] = p[2] 
    else:
        p[0] = [] 

def p_classe_body(p):
    """classe_body : LBRACE RBRACE
                   | empty"""
    if len(p) == 3:
        p[0] = {"type": "ClassBody", "attributes": []} 
    else:
        p[0] = None 

def p_lista_nomes_classe(p):
    """lista_nomes_classe : CLASS_NAME COMMA lista_nomes_classe
                          | CLASS_NAME"""
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_estereotipo_classe(p):
    """estereotipo_classe : EVENT
                           | SITUATION
                           | PROCESS
                           | CATEGORY
                           | MIXIN
                           | PHASEMIXIN
                           | ROLEMIXIN
                           | HISTORICALROLEMIXIN
                           | KIND
                           | COLLECTIVE
                           | QUANTITY
                           | QUALITY
                           | MODE
                           | INTRISICMODE
                           | EXTRINSICMODE
                           | SUBKIND
                           | PHASE
                           | ROLE
                           | HISTORICALROLE"""
    p[0] = p[1]

# ----------------------------------
# F. (NOVO) DECLARAÇÃO DE ENUM (CONSTRUTO 4)
# ----------------------------------

def p_declaracao_enum(p):
    """declaracao_enum : ENUM CLASS_NAME LBRACE lista_individuos RBRACE"""
    p[0] = {
        "type": "EnumDeclaration",
        "name": p[2],
        "members": p[4] # p[4] vem da 'lista_individuos'
    }

# Regra auxiliar para a lista de membros do enum
# Nota: Usamos CLASS_NAME aqui, pois o lexer os classifica assim.
def p_lista_individuos(p):
    """lista_individuos : CLASS_NAME COMMA lista_individuos
                        | CLASS_NAME"""
    if len(p) == 4:
        # Ex: Blue, Green...
        p[0] = [p[1]] + p[3]
    else:
        # Ex: Blue (último ou único da lista)
        p[0] = [p[1]]


# =============================================================================
# 3. FUNÇÃO VAZIA E TRATAMENTO DE ERROS
# =============================================================================
def p_empty(p):
    """empty :"""
    pass

global has_error
has_error = False

def p_error(p):
    """Tratamento de erro sintático."""
    global has_error
    has_error = True
    if p:
        print(
            f"\n[ERRO SINTÁTICO] Token inesperado: {p.type} ('{p.value}') na linha {p.lineno}"
        )
    else:
        print(
            "\n[ERRO SINTÁTICO] Fim de arquivo inesperado (EOF). O código está incompleto."
        )

# =============================================================================
# 4. CONSTRUÇÃO DO PARSER
# =============================================================================
parser = yacc.yacc()

# Função auxiliar para ser chamada pelo main.py
def parse_tonto_code(code_string):
    """
    Função principal para analisar o código TONTO.
    Retorna a Árvore Sintática Abstrata (AST) ou None se houver erros.
    """
    global has_error
    has_error = False
    
    # Zera o lexer (importante para múltiplas execuções)
    lexer.lineno = 1
    
    # Chama o parser
    ast_result = parser.parse(code_string, lexer=lexer)
    
    if has_error:
        return None
    
    return ast_result