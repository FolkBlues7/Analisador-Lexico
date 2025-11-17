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
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

# ----------------------------------
# D. HUB DE DECLARAÇÕES
# ----------------------------------
def p_declaracao(p):
    """declaracao : declaracao_classe
                   | declaracao_enum
                   | declaracao_datatype
                   | declaracao_genset""" # <-- (NOVO) Adicionado genset ao hub
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
# F. DECLARAÇÃO DE ENUM (CONSTRUTO 4)
# ----------------------------------
def p_declaracao_enum(p):
    """declaracao_enum : ENUM CLASS_NAME LBRACE lista_individuos RBRACE"""
    p[0] = {
        "type": "EnumDeclaration",
        "name": p[2],
        "members": p[4]
    }

def p_lista_individuos(p):
    """lista_individuos : CLASS_NAME COMMA lista_individuos
                        | CLASS_NAME"""
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

# ----------------------------------
# G. DECLARAÇÃO DE DATATYPE (CONSTRUTO 3)
# ----------------------------------
def p_declaracao_datatype(p):
    """declaracao_datatype : DATATYPE CLASS_NAME LBRACE lista_atributos_datatype RBRACE"""
    p[0] = {
        "type": "DataTypeDeclaration",
        "name": p[2],
        "attributes": p[4]
    }

def p_lista_atributos_datatype(p):
    """lista_atributos_datatype : atributo_datatype COMMA lista_atributos_datatype
                                | atributo_datatype
                                | empty"""
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2 and p[1] is not None: # p[1] pode ser None se a regra for 'empty'
        p[0] = [p[1]]
    else:
        p[0] = []

def p_atributo_datatype(p):
    """atributo_datatype : RELATION_NAME COLON tipo_atributo"""
    p[0] = {
        "type": "Attribute",
        "name": p[1],
        "datatype": p[3]
    }

def p_tipo_atributo(p):
    """tipo_atributo : tipo_primitivo
                     | CLASS_NAME"""
    p[0] = p[1]

def p_tipo_primitivo(p):
    """tipo_primitivo : NUMBER_TYPE
                      | STRING_TYPE
                      | BOOLEAN_TYPE
                      | DATE_TYPE
                      | TIME_TYPE
                      | DATETIME_TYPE
                      | INT_TYPE"""
    p[0] = p[1]

# ----------------------------------
# H. (NOVO) DECLARAÇÃO DE GENSET (CONSTRUTO 5)
# ----------------------------------

# Regra principal
def p_declaracao_genset(p):
    """declaracao_genset : genset_modifiers GENSET CLASS_NAME genset_form"""
    # p[1] = lista de modificadores (ex: ['disjoint', 'complete'])
    # p[3] = nome do genset (ex: 'AgePhase')
    # p[4] = dicionário com {general, specifics, form}
    p[0] = {
        "type": "GeneralizationSet",
        "name": p[3],
        "modifiers": p[1],
        **p[4] # Desempacota o dicionário de p[4]
    }

# Regra para os modificadores opcionais
def p_genset_modifiers(p):
    """genset_modifiers : genset_modifier genset_modifiers
                        | empty"""
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

# Regra para um único modificador
def p_genset_modifier(p):
    """genset_modifier : DISJOINT
                       | COMPLETE"""
    p[0] = p[1] # Retorna a string 'disjoint' or 'complete'

# Regra para escolher entre a forma 'where' ou 'block'
def p_genset_form(p):
    """genset_form : genset_form_where
                   | genset_form_block"""
    p[0] = p[1] # Apenas repassa o dicionário

# Regra para a forma 'where'
def p_genset_form_where(p):
    """genset_form_where : WHERE lista_nomes_classe SPECIALIZES CLASS_NAME"""
    # Reutilizamos a 'lista_nomes_classe' que já tínhamos!
    p[0] = {
        "form": "where",
        "general": p[4],
        "specifics": p[2]
    }

# Regra para a forma 'block'
def p_genset_form_block(p):
    """genset_form_block : LBRACE GENERAL CLASS_NAME SPECIFICS lista_nomes_classe RBRACE"""
    p[0] = {
        "form": "block",
        "general": p[3],
        "specifics": p[5]
    }


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