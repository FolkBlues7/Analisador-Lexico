import ply.yacc as yacc
import json 

# =============================================================================
# 1. IMPORTAÇÃO DOS TOKENS E LEXER
# =============================================================================
try:
    # Ajuste o caminho de importação conforme a estrutura real do seu projeto
    from lexer.lexer import tokens, lexer 
except ImportError:
    print("[ERRO FATAL] Não foi possível importar a lista de tokens do seu lexer. Por favor, verifique o caminho.")
    exit(1)

# =============================================================================
# 2. REGRAS DE GRAMÁTICA (TONTO - Estrutura de Pacotes)
# =============================================================================

# ----------------------------------
# A. REGRA PRINCIPAL AJUSTADA (Força o Pacote)
# ----------------------------------
def p_programa(p):
    '''programa : pre_package_decls declaracao_package declaracoes_pos_package'''
    
    # p[1] é a lista de imports
    # p[2] é a ÚNICA declaração de Package
    # p[3] são as outras declarações (Classes, Relações, etc.)
    
    # Constrói o nó raiz da AST
    p[0] = {
        'type': 'OntologyModel',
        'imports': p[1],
        'package': p[2],
        'declarations': p[3]
    }

# ----------------------------------
# B. SEÇÃO PRÉ-PACKAGE (Imports Opcionais)
# ----------------------------------
def p_pre_package_decls(p):
    '''pre_package_decls : pre_package_decls import_decl
                         | empty'''
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
    '''import_decl : IMPORT CLASS_NAME''' # Assumimos que o nome do pacote importado é um CLASS_NAME
    p[0] = {
        'type': 'ImportDeclaration',
        'package_name': p[2],
        'lineno': p.lineno(1)
    }

# ----------------------------------
# C. REGRA 1: DECLARAÇÃO DE PACOTES (Obrigatória, no início do corpo)
# ----------------------------------
# Sintaxe esperada: 'package' <CLASS_NAME>
def p_declaracao_package(p):
    '''declaracao_package : PACKAGE CLASS_NAME''' 
    
    # Constrói o nó da AST
    p[0] = {
        'type': 'PackageDeclaration',
        'name': p[2],
        'lineno': p.lineno(1)
    }

# ----------------------------------
# D. DECLARAÇÕES PÓS-PACKAGE (Classes, Relações, Gensets - Opcionais)
# ----------------------------------
def p_declaracoes_pos_package(p):
    '''declaracoes_pos_package : declaracoes_pos_package declaracao_restante
                               | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    elif p[1] != None:
        p[0] = [p[1]]
    else:
        p[0] = []

# Placeholder para todas as futuras declarações (Classes, Relações, etc.)
def p_declaracao_restante(p):
    '''declaracao_restante : tipo_simples CLASS_NAME
                           | declaracao_genset
                           | declaracao_relacao'''
    # Aqui você retornará o nó da AST da declaração, mas por enquanto, apenas um placeholder
    p[0] = {'type': 'WIP_Declaration', 'value': p[1]} # Placeholder

# Placeholder simples para garantir que a gramática não quebre
def p_tipo_simples(p):
    '''tipo_simples : KIND'''
    p[0] = {'type': 'ClassDeclaration', 'stereotype': p[1]}

def p_declaracao_genset(p):
    '''declaracao_genset : GENSET CLASS_NAME'''
    p[0] = {'type': 'GensetDeclaration (WIP)'}
    
def p_declaracao_relacao(p):
    '''declaracao_relacao : RELATION_NAME'''
    p[0] = {'type': 'RelationDeclaration (WIP)'}

# ----------------------------------
# E. FUNÇÃO VAZIA E ERRO
# ----------------------------------
def p_empty(p):
    'empty :'
    pass

global has_error
has_error = False

def p_error(p):
    """Tratamento de erro sintático."""
    global has_error
    has_error = True
    if p:
        print(f"\n[ERRO SINTÁTICO] Token inesperado: {p.type} ('{p.value}') na linha {p.lineno}")
    else:
        print("\n[ERRO SINTÁTICO] Fim de arquivo inesperado (EOF). O código está incompleto.")

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
#Cada modelo em Tonto precisa começar com a declaração de um pacote" 
#(permitindo apenas imports opcionais antes).

# ----------------------------------
# D. DECLARAÇÕES PÓS-PACKAGE (Classes, Relações, Gensets - Opcionais)
# ----------------------------------
# ... (manter p_declaracoes_pos_package)

# ATUALIZAÇÃO: Adicionando suporte à declaração de classes completa
def p_declaracao_restante(p):
    '''declaracao_restante : declaracao_classe_completa
                           | declaracao_genset
                           | declaracao_relacao'''
    p[0] = p[1] # Retorna o resultado da regra chamada

# ----------------------------------
# E. REGRAS PARA DECLARAÇÃO DE CLASSES (Requisito 2)
# ----------------------------------

# Esta é a regra central que cobre as diversas formas de declarar classes
def p_declaracao_classe_completa(p):
    '''declaracao_classe_completa : tipo_simples CLASS_NAME corpo_classe
                                  | tipo_simples CLASS_NAME SPECIALIZES CLASS_NAME corpo_classe
                                  | tipo_com_especializacao CLASS_NAME SPECIALIZES CLASS_NAME corpo_classe
                                  | tipo_com_modificador CLASS_NAME corpo_classe'''
    
    # Lógica para extrair as partes, dependendo do número de elementos (simplificado):
    if len(p) == 4: # tipo CLASS_NAME corpo
        stereotype, name, body = p[1], p[2], p[3]
        specializes = None
    elif len(p) == 5: # tipo CLASS_NAME SPECIALIZES CLASS_NAME corpo (Assumindo que SPECIALIZES é opcionalmente seguido de corpo)
        stereotype, name, specializes, body = p[1], p[2], p[4], None # Corrigir a lógica de AST aqui se SPECIALIZES não estiver lá.
        # Devido à complexidade de misturar SPECIALIZES e corpo na mesma regra, vamos separar o corpo.
        
        # O melhor é reescrever, tratando o corpo como OPCIONAL:
        if p[3] == '{': # tipo CLASS_NAME { ... }
             stereotype, name, body = p[1], p[2], p[4]
             specializes = None
        else: # tipo CLASS_NAME SPECIALIZES CLASS_NAME
             stereotype, name, specializes = p[1], p[2], p[4]
             body = {'attributes': [], 'relations': []} # Corpo vazio
    
    # Vamos simplificar as regras para cobrir os dois exemplos:
    
    # 1. kind Person { ... }
    if len(p) == 4:
        p[0] = {
            'type': 'ClassDeclaration',
            'stereotype': p[1]['stereotype'],
            'name': p[2],
            'specializes': None,
            'body': p[3],
            'lineno': p.lineno(1)
        }
    # 2. phase Child specializes Person
    elif len(p) == 5: # tipo CLASS_NAME SPECIALIZES CLASS_NAME
         p[0] = {
            'type': 'ClassDeclaration',
            'stereotype': p[1]['stereotype'],
            'name': p[2],
            'specializes': p[4],
            'body': {'attributes': [], 'relations': []}, # Corpo vazio
            'lineno': p.lineno(1)
        }
    # NOTA: O tratamento do corpo da classe com LBRACE/RBRACE será tratado abaixo.

# Estereótipos de classe simples (KIND, EVENT, etc.)
def p_tipo_simples(p):
    '''tipo_simples : KIND 
                    | EVENT 
                    | SITUATION
                    | PROCESS
                    | CATEGORY
                    | COLLECTIVE
                    | QUANTITY
                    | QUALITY
                    | MODE'''
    p[0] = {'type': 'ClassDeclaration', 'stereotype': p[1]}

# Estereótipos de classe que indicam sub-tipagem (SUBKIND, PHASE, ROLE)
def p_tipo_com_especializacao(p):
    '''tipo_com_especializacao : SUBKIND
                               | PHASE
                               | ROLE
                               | HISTORICALROLE'''
    p[0] = {'type': 'ClassDeclaration', 'stereotype': p[1]}
    
# Estereótipos que atuam como modificadores (MIXIN, PHASEMIXIN, etc.)
def p_tipo_com_modificador(p):
    '''tipo_com_modificador : MIXIN
                            | PHASEMIXIN
                            | ROLEMIXIN
                            | HISTORICALROLEMIXIN
                            | INTRISICMODE
                            | EXTRINSICMODE'''
    p[0] = {'type': 'ClassDeclaration', 'stereotype': p[1]}

# ----------------------------------
# F. REGRAS PARA O CORPO DA CLASSE (Atributos e Declarações Internas)
# ----------------------------------

# O corpo da classe é opcional (pode ser {}) ou pode ser omitido se houver SPECIALIZES
def p_corpo_classe(p):
    '''corpo_classe : LBRACE lista_membros RBRACE
                    | empty'''
    if len(p) == 4:
        p[0] = {'attributes': p[2]['attributes'], 'relations': p[2]['relations']}
    else:
        p[0] = {'attributes': [], 'relations': []}

# Lista de membros dentro do corpo (atributos, ou futuras relações internas)
def p_lista_membros(p):
    '''lista_membros : lista_membros membro
                     | membro'''
    
    if len(p) == 3: # recursivo
        # p[1] é a lista de membros atual, p[2] é o novo membro
        # Usamos p[1] para acumular a lista
        if p[2]['type'] == 'Attribute':
             p[1]['attributes'].append(p[2])
        elif p[2]['type'] == 'InternalRelation':
             p[1]['relations'].append(p[2])
        p[0] = p[1]
    else: # base
        # Inicializa a lista de membros
        p[0] = {'attributes': [], 'relations': []}
        if p[1]['type'] == 'Attribute':
             p[0]['attributes'].append(p[1])
        elif p[1]['type'] == 'InternalRelation':
             p[0]['relations'].append(p[1])

# Um membro pode ser um atributo ou uma relação interna
def p_membro(p):
    '''membro : declaracao_atributo
              | declaracao_relacao_interna'''
    p[0] = p[1]


# ----------------------------------
# G. DECLARAÇÃO DE ATRIBUTOS
# ----------------------------------

# Sintaxe: <RELATION_NAME>: <TYPE> <meta_atributos_opcional>
def p_declaracao_atributo(p):
    '''declaracao_atributo : RELATION_NAME COLON tipo_atributo meta_atributos_opcional'''
    
    p[0] = {
        'type': 'Attribute',
        'name': p[1],
        'data_type': p[3],
        'meta_attributes': p[4],
        'lineno': p.lineno(1)
    }

# Tipos de Atributos: Tipos Nativos (string, date) ou Novos Tipos (NEW_DATATYPE)
def p_tipo_atributo(p):
    '''tipo_atributo : NUMBER_TYPE
                     | STRING_TYPE
                     | BOOLEAN_TYPE
                     | DATE_TYPE
                     | TIME_TYPE
                     | DATETIME_TYPE
                     | NEW_DATATYPE'''
    p[0] = p[1] # Retorna o nome do tipo (e.g., 'string')

# Meta-Atributos Opcionais para Atributos: { const }
def p_meta_atributos_opcional(p):
    '''meta_atributos_opcional : LBRACE meta_atributos_lista RBRACE
                               | empty'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = []

# Meta-atributos suportados para um atributo
def p_meta_atributos_lista(p):
    '''meta_atributos_lista : CONST
                            | meta_atributos_lista COMMA CONST'''
    
    # Simplificação: Apenas retorna uma lista de strings para os meta-atributos
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


# ----------------------------------
# H. PLACEHOLDERS ADICIONAIS
# ----------------------------------
# Placeholder para relações internas (futuro)
def p_declaracao_relacao_interna(p):
    '''declaracao_relacao_interna : RELATION_NAME LBRACKET RBRACKET''' # Ex: myRel[1..*]
    p[0] = {'type': 'InternalRelation', 'name': p[1]} # Placeholder

# ... (manter p_declaracao_genset, p_declaracao_relacao e p_empty)

#########################################################################
# ----------------------------------
# D. DECLARAÇÕES PÓS-PACKAGE (Classes, Relações, Gensets, DATATYPES - Opcionais)
# ----------------------------------

# ATUALIZAÇÃO: Incluindo a nova regra 'declaracao_datatype'
def p_declaracao_restante(p):
    '''declaracao_restante : declaracao_classe_completa
                           | declaracao_datatype # NOVO: Declaração de Tipos de Dados
                           | declaracao_genset
                           | declaracao_relacao'''
    p[0] = p[1] 

# ----------------------------------
# E. NOVO REQUISITO: DECLARAÇÃO DE TIPOS DE DADOS (DATATYPE)
# ----------------------------------
# Estrutura: 'datatype' <CLASS_NAME> { <lista_atributos> }
def p_declaracao_datatype(p):
    '''declaracao_datatype : DATATYPE CLASS_NAME LBRACE lista_atributos RBRACE'''
    
    # Reutilizamos a lógica da lista de atributos, mas simplificamos o retorno.
    p[0] = {
        'type': 'DataTypeDeclaration',
        'name': p[2],
        'attributes': p[4]['attributes'], # Lista de atributos (reutiliza a estrutura de membros)
        'lineno': p.lineno(1)
    }

# O tipo de declaração de membro dentro de um datatype é restrito apenas a atributos.
# A função 'p_lista_membros' e 'p_declaracao_atributo' já suportam o conteúdo
# (e.g., street: string e number: int) pois a estrutura interna é idêntica à de uma classe.

# ATENÇÃO: É necessário garantir que p_lista_membros não tente adicionar Relações
# se for usado em p_declaracao_datatype. Vamos refatorar a lista de atributos para ser 
# mais específica para Tipos de Dados e Classes.

# --- REORGANIZAÇÃO PARA REUTILIZAÇÃO DE CÓDIGO ---

# A Lista de Atributos é a mesma tanto para Classes quanto para DataTypes.
def p_lista_atributos(p):
    '''lista_atributos : lista_atributos declaracao_atributo
                       | declaracao_atributo'''
    
    if len(p) == 3: # recursivo
        # p[1] é a lista de atributos (acumula), p[2] é o novo atributo
        p[0] = p[1] + [p[2]]
    else: # base
        # Inicializa a lista com o primeiro atributo
        p[0] = [p[1]]

# Reajustando a Regra do Corpo da Classe para usar a nova lista_atributos
def p_corpo_classe(p):
    '''corpo_classe : LBRACE lista_atributos_e_relacoes RBRACE
                    | empty'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = {'attributes': [], 'relations': []}
        
# Nova Regra para o Corpo da Classe que pode conter ATRIBUTOS E RELAÇÕES
def p_lista_atributos_e_relacoes(p):
    '''lista_atributos_e_relacoes : lista_atributos_e_relacoes membro
                                  | membro'''
    
    # Inicializa o acumulador de listas
    if len(p) == 2: # Caso base
        p[0] = {'attributes': [], 'relations': []}
        membro = p[1]
    else: # Caso recursivo
        p[0] = p[1] # Acumulador
        membro = p[2]

    # Classifica o membro
    if membro['type'] == 'Attribute':
         p[0]['attributes'].append(membro)
    elif membro['type'] == 'InternalRelation':
         p[0]['relations'].append(membro)
         
# O resto das regras (membro, declaracao_atributo, tipo_atributo, etc.)
# permanecem as mesmas, pois a sintaxe interna é idêntica: <nome>: <tipo> {<meta>}

# ... (Manter p_declaracao_atributo, p_tipo_atributo, etc., sem alterações)