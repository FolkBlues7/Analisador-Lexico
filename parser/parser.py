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
# 2. REGRAS DE GRAMÁTICA (TONTO - Estrutura de Pacotes)
# =============================================================================


# ----------------------------------
# A. REGRA PRINCIPAL AJUSTADA (Força o Pacote)
# ----------------------------------
def p_programa(p):
    """programa : pre_package_decls declaracao_package declaracoes_pos_package"""

    # p[1] é a lista de imports
    # p[2] é a ÚNICA declaração de Package
    # p[3] são as outras declarações (Classes, Relações, etc.)

    # Constrói o nó raiz da AST
    p[0] = {
        "type": "OntologyModel",
        "imports": p[1],
        "package": p[2],
        "declarations": p[3],
    }


# ----------------------------------
# B. SEÇÃO PRÉ-PACKAGE (Imports Opcionais)
# ----------------------------------
def p_pre_package_decls(p):
    """pre_package_decls : pre_package_decls import_decl
    | empty"""
    if len(p) == 3:
        # Caso recursivo: Adiciona a nova importação à lista
        p[0] = p[1] + [p[2]]
    elif p[1] != None:
        # Caso base: [import_decl]
        p[0] = [p[1]]
    else:
        # Caso empty
        p[0] = []


# REGRA IMPORT: Importa um pacote externo
# Sintaxe esperada: 'import' <CLASS_NAME ou ID>
def p_import_decl(p):
    """import_decl : IMPORT CLASS_NAME"""  # Assumimos que o nome do pacote importado é um CLASS_NAME
    p[0] = {"type": "ImportDeclaration", "package_name": p[2], "lineno": p.lineno(1)}


# ----------------------------------
# C. REGRA 1: DECLARAÇÃO DE PACOTES (Obrigatória, no início do corpo)
# ----------------------------------
# Sintaxe esperada: 'package' <CLASS_NAME>
def p_declaracao_package(p):
    """declaracao_package : PACKAGE CLASS_NAME"""

    # Constrói o nó da AST
    p[0] = {"type": "PackageDeclaration", "name": p[2], "lineno": p.lineno(1)}


# ----------------------------------
# D. DECLARAÇÕES PÓS-PACKAGE (CONSOLIDADO E CORRIGIDO)
# ----------------------------------
def p_declaracoes_pos_package(p):
    """declaracoes_pos_package : declaracoes_pos_package declaracao_restante
    | empty"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []


# Consolida todas as declarações permitidas: CLASSES, DATATYPES, RELATOR, GENSET
def p_declaracao_restante(p):
    """declaracao_restante : declaracao_classe_completa
    | declaracao_datatype
    | declaracao_genset
    | declaracao_relacao_placeholder"""
    p[0] = p[1]


# ----------------------------------
# E. DECLARAÇÃO DE TIPOS DE DADOS (Requisito 3)
# ----------------------------------
def p_declaracao_datatype(p):
    """declaracao_datatype : DATATYPE CLASS_NAME LBRACE lista_atributos RBRACE"""

    p[0] = {
        "type": "DataTypeDeclaration",
        "name": p[2],
        "attributes": p[4],  # p[4] é o resultado da lista de atributos
        "lineno": p.lineno(1),
    }


# ----------------------------------
# F. REGRAS PARA DECLARAÇÃO DE CLASSES (Requisito 2: CORRIGIDO)
# ----------------------------------


# Esta regra lida com todos os estereótipos, especialização e corpo
def p_declaracao_classe_completa(p):
    """declaracao_classe_completa : tipo_qualquer CLASS_NAME clausula_especializacao_opcional corpo_classe"""

    p[0] = {
        "type": "ClassDeclaration",
        "stereotype": p[1]["stereotype"],
        "name": p[2],
        "specializes": p[
            3
        ],  # Lista de supertipos (Resultado de p_clausula_especializacao_opcional)
        "body": p[4],
        "lineno": p.lineno(1),
    }


# Combina todos os estereótipos em uma só regra (Corrigindo o problema de '|')
def p_tipo_qualquer(p):
    """tipo_qualquer : KIND
    | EVENT
    | SITUATION
    | PROCESS
    | CATEGORY
    | COLLECTIVE
    | QUANTITY
    | QUALITY
    | MODE
    | SUBKIND
    | PHASE
    | ROLE
    | HISTORICALROLE
    | MIXIN
    | PHASEMIXIN
    | ROLEMIXIN
    | HISTORICALROLEMIXIN
    | INTRISICMODE
    | EXTRINSICMODE"""
    p[0] = {"type": "ClassStereotype", "stereotype": p[1]}


def p_estereotipo_relacao(p):
    """estereotipo_relacao : MATERIAL
    | DERIVATION
    | COMPARATIVE
    | MEDIATION
    | CHARACTERIZATION
    | EXTERNALDEPENDENCE
    | COMPONENTOF
    | MEMBEROF
    | SUBCOLLECTIONOF
    | SUBQUALITYOF
    | INSTANTIATION
    | TERMINATION
    | PARTICIPATIONAL
    | PARTICIPATION
    | HISTORICALDEPENDENCE
    | CREATION
    | MANIFESTATION
    | BRINGSABOUT
    | TRIGGERS
    | COMPOSITION
    | AGGREGATION
    | INHERENCE
    | VALUE
    | FORMAL
    | CONSTITUTION"""
    p[0] = p[1]


# NOVO CÓDIGO CORRIGIDO (Adicione esta regra)
def p_genset_propriedades_opcionais(p):
    """genset_propriedades_opcionais : disjoint_opcional complete_opcional"""
    p[0] = {"is_disjoint": p[1], "is_complete": p[2]}


def p_disjoint_opcional(p):
    """disjoint_opcional : DISJOINT
    | empty"""
    p[0] = len(p) > 1


def p_complete_opcional(p):
    """complete_opcional : COMPLETE
    | empty"""
    p[0] = len(p) > 1


# Cláusula 'specializes SuperTipo' (Corrigida e Simplificada)
def p_clausula_especializacao_opcional(p):
    """clausula_especializacao_opcional : SPECIALIZES lista_super_tipos
    | empty"""
    if len(p) == 3:
        p[0] = p[2]  # Retorna a lista de super-tipos
    else:
        p[0] = []  # Retorna lista vazia


def p_lista_super_tipos(p):
    """lista_super_tipos : CLASS_NAME
    | lista_super_tipos COMMA CLASS_NAME"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


# ----------------------------------
# G. REGRAS PARA O CORPO, ATRIBUTOS E RELAÇÕES INTERNAS
# ----------------------------------


# O corpo da classe é opcional
def p_corpo_classe(p):
    """corpo_classe : LBRACE lista_atributos_e_relacoes RBRACE
    | empty"""
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = {"attributes": [], "relations": []}


# Lista de Atributos (usado em DataTypes)
def p_lista_atributos(p):
    """lista_atributos : lista_atributos declaracao_atributo
    | declaracao_atributo
    | empty"""
    # Apenas retorna a lista de atributos (corrigido para ter 'empty')
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    elif len(p) == 2 and p[1] != None:
        p[0] = [p[1]]
    else:
        p[0] = []


# Lista de Atributos E Relações Internas (usado em Classes)
def p_lista_atributos_e_relacoes(p):
    """lista_atributos_e_relacoes : lista_atributos_e_relacoes membro
    | membro
    | empty"""

    if len(p) == 2:
        if p[1] == None:  # empty
            p[0] = {"attributes": [], "relations": []}
        else:  # caso base: 1 membro
            p[0] = {"attributes": [], "relations": []}
            membro = p[1]
            if membro["type"] == "Attribute":
                p[0]["attributes"].append(membro)
            elif membro["type"] == "InternalRelation":
                p[0]["relations"].append(membro)
    elif len(p) == 3:  # caso recursivo
        p[0] = p[1]
        membro = p[2]
        if membro["type"] == "Attribute":
            p[0]["attributes"].append(membro)
        elif membro["type"] == "InternalRelation":
            p[0]["relations"].append(membro)
    else:  # Caso "empty" (se não for capturado pelo len=2)
        p[0] = {"attributes": [], "relations": []}


def p_membro(p):
    """membro : declaracao_atributo
    | declaracao_relacao_interna"""
    p[0] = p[1]


# Declaração de Atributos (Mantido)
def p_declaracao_atributo(p):
    """declaracao_atributo : RELATION_NAME COLON tipo_atributo meta_atributos_opcional"""

    p[0] = {
        "type": "Attribute",
        "name": p[1],
        "data_type": p[3],
        "meta_attributes": p[4],
        "lineno": p.lineno(1),
    }


# Tipos de Atributos (Mantido, corrigindo o problema de '|')
def p_tipo_atributo(p):
    """tipo_atributo : NUMBER_TYPE
    | STRING_TYPE
    | BOOLEAN_TYPE
    | DATE_TYPE
    | TIME_TYPE
    | DATETIME_TYPE
    | NEW_DATATYPE"""
    p[0] = p[1]


# Meta-Atributos Opcionais para Atributos: { const } (Mantido)
def p_meta_atributos_opcional(p):
    """meta_atributos_opcional : LBRACE meta_atributos_lista RBRACE
    | empty"""
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = []


# Meta-atributos suportados para um atributo (Mantido)
def p_meta_atributos_lista(p):
    """meta_atributos_lista : CONST
    | meta_atributos_lista COMMA CONST"""

    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


# ----------------------------------
# H. PLACEHOLDERS (Corrigidos)
# ----------------------------------
def p_declaracao_relacao_interna(p):
    """declaracao_relacao_interna : RELATION_NAME LBRACKET RBRACKET
    | RELATION_NAME LBRACKET NUMBER DOTDOT ASTERISK RBRACKET
    | RELATION_NAME LBRACKET NUMBER RBRACKET"""
    p[0] = {"type": "InternalRelation", "name": p[1]}


# NOVO CÓDIGO CORRIGIDO (Substitua p_declaracao_genset)
def p_declaracao_genset(p):
    """declaracao_genset : genset_head CLASS_NAME LBRACE lista_membros_genset RBRACE"""

    p[0] = {
        "type": "GensetDeclaration",
        "name": p[2],
        "properties": p[1],  # Resultado de genset_head
        "members": p[4],
        "lineno": p.lineno(1),
    }


# NOVO CÓDIGO (Adicione esta regra)
# NOVO CÓDIGO (Corrigido)
def p_genset_head(p):
    """genset_head : disjoint_opcional complete_opcional GENSET"""

    # Este é o bloco de código CORRETO
    # p[1] = is_disjoint (bool), p[2] = is_complete (bool)
    p[0] = {"is_disjoint": p[1], "is_complete": p[2]}


# NOVO CÓDIGO CORRIGIDO (p_lista_membros_genset)
# ESTE É O CÓDIGO FINAL CORRETO PARA A FUNÇÃO
def p_lista_membros_genset(p):
    """lista_membros_genset : lista_membros_genset membro_genset
    | membro_genset"""

    if len(p) == 3:  # Caso recursivo: lista acumulada + novo membro
        # p[1] é a lista, p[2] é o novo elemento
        p[0] = p[1] + [p[2]]
    else:  # Caso base: Apenas um membro
        # p[0] é uma lista contendo o primeiro elemento
        p[0] = [p[1]]


# NOVO CÓDIGO CORRIGIDO (p_membro_genset)
def p_membro_genset(p):
    """membro_genset : GENERAL CLASS_NAME
    | SPECIFICS lista_super_tipos"""

    # IMPORTANTE: Acessar a palavra-chave original com p[1]
    if p[1] == "GENERAL":
        p[0] = {"type": "GensetMember", "role": "general", "name": p[2]}
    elif p[1] == "SPECIFICS":
        p[0] = {"type": "GensetMember", "role": "specifics", "names": p[2]}


def p_membro_genset_placeholder(p):
    """membro_genset_placeholder : GENERAL CLASS_NAME
    | SPECIFICS lista_super_tipos"""
    p[0] = {"type": "GensetMemberPlaceholder"}


# Placeholder para Relator (REQUER O TOKEN 'RELATOR')
def p_declaracao_relacao_placeholder(p):
    """declaracao_relacao_placeholder : RELATOR CLASS_NAME LBRACE lista_terminacoes_vazia RBRACE"""
    p[0] = {"type": "RelationPlaceholder", "name": p[2]}


def p_lista_terminacoes_vazia(p):
    """lista_terminacoes_vazia : lista_terminacoes_vazia terminacao_relacao_vazia
    | terminacao_relacao_vazia
    | empty"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    elif len(p) == 2 and p[1] != None:
        p[0] = [p[1]]
    else:
        p[0] = []


# Esta regra tenta casar com a sintaxe de terminação de relator
def p_terminacao_relacao_vazia(p):
    """terminacao_relacao_vazia : AT estereotipo_relacao DOUBLE_HYPHEN RELATION_NAME DOUBLE_HYPHEN LBRACKET NUMBER RBRACKET CLASS_NAME"""
    p[0] = {"type": "RelationTerminationPlaceholder"}


# ----------------------------------
# I. FUNÇÃO VAZIA E ERRO (MANTIDO)
# ----------------------------------
def p_empty(p):
    "empty :"
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
# 3. CONSTRUÇÃO E EXPORTAÇÃO DO PARSER
# =============================================================================
parser = yacc.yacc()


def parse_tonto_code(code):
    """Função principal de parse para ser chamada na main.py"""
    global has_error
    has_error = False

    lexer.lineno = 1

    result = parser.parse(code, lexer=lexer)

    if not has_error:
        return result
    else:
        return None
