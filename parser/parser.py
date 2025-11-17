import ply.yacc as yacc
import json

# =============================================================================
# 1. IMPORTAÇÃO DOS TOKNES E LEXER
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
# C. (NOVO) LISTA DE DECLARAÇÕES PÓS-PACOTE
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
# D. (NOVO) HUB DE DECLARAÇÕES
# ----------------------------------
def p_declaracao(p):
    """declaracao : declaracao_classe"""
    # Este é o "hub". Por enquanto, ele só chama 'declaracao_classe'.
    # No futuro, adicionaremos:
    # declaracao : declaracao_classe
    #            | declaracao_enum
    #            | declaracao_genset
    #            | ...
    p[0] = p[1]

# ----------------------------------
# E. (NOVO) DECLARAÇÃO DE CLASSE (CONSTRUTO 2)
# ----------------------------------

# Esta é a regra principal para uma classe.
# Uma classe tem:
# 1. Um estereótipo (kind, phase, role, etc.)
# 2. Um nome (CLASS_NAME)
# 3. Uma especialização (opcional)
# 4. Um corpo (opcional)
def p_declaracao_classe(p):
    """declaracao_classe : estereotipo_classe CLASS_NAME classe_specialization classe_body"""
    p[0] = {
        "type": "ClassDeclaration",
        "stereotype": p[1],
        "name": p[2],
        "specializes": p[3], # p[3] vem da regra 'classe_specialization'
        "body": p[4]         # p[4] vem da regra 'classe_body'
    }

# Regra para a parte opcional de especialização
def p_classe_specialization(p):
    """classe_specialization : SPECIALIZES lista_nomes_classe
                             | empty"""
    if len(p) == 3:
        p[0] = p[2] # Retorna a lista de classes das quais ela especializa
    else:
        p[0] = [] # Retorna uma lista vazia se não houver 'specializes'

# Regra para a parte opcional do corpo
def p_classe_body(p):
    """classe_body : LBRACE RBRACE
                   | empty"""
    # NOTA: Por enquanto, o corpo está VAZIO.
    # Em etapas futuras, colocaremos as declarações de atributos aqui.
    if len(p) == 3:
        p[0] = {"type": "ClassBody", "attributes": []} # Um corpo {}
    else:
        p[0] = None # Nenhum corpo

# Regra auxiliar para 'lista_nomes_classe' (ex: specializes Person, Customer)
def p_lista_nomes_classe(p):
    """lista_nomes_classe : CLASS_NAME COMMA lista_nomes_classe
                          | CLASS_NAME"""
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

# Regra auxiliar para agrupar todos os estereótipos de classe válidos
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
    p[0] = p[1] # Retorna a própria string do token (ex: 'kind')


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
        # (Futuramente, podemos adicionar sugestões aqui)
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