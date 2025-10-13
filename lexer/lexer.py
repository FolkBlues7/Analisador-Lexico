import ply.lex as lex

# -----------------------------------------------------------------------------
# 1. LISTA DE TOKENS E PALAVRAS RESERVADAS
# -----------------------------------------------------------------------------

# Palavras reservadas, estereótipos e meta-atributos da linguagem TONTO
reserved = {
    # Palavras-chave da estrutura
    'package': 'PACKAGE', 'class': 'CLASS', 'datatype': 'DATATYPE', 'attributes': 'ATTRIBUTES',
    'associations': 'ASSOCIATIONS', 'generalizations': 'GENERALIZATIONS', 'genset': 'GENSET',
    'disjoint': 'DISJOINT', 'complete': 'COMPLETE', 'general': 'GENERAL', 'specifics': 'SPECIFICS',
    'where': 'WHERE',

    # Estereótipos de Classe
    'event': 'EVENT', 'situation': 'SITUATION', 'process': 'PROCESS', 'category': 'CATEGORY',
    'mixin': 'MIXIN', 'phaseMixin': 'PHASEMIXIN', 'roleMixin': 'ROLEMIXIN',
    'historicalRoleMixin': 'HISTORICALROLEMIXIN', 'kind': 'KIND', 'collective': 'COLLECTIVE',
    'quantity': 'QUANTITY', 'quality': 'QUALITY', 'mode': 'MODE', 'intrisicMode': 'INTRISICMODE',
    'extrinsicMode': 'EXTRINSICMODE', 'subkind': 'SUBKIND', 'phase': 'PHASE', 'role': 'ROLE',
    'historicalRole': 'HISTORICALROLE',

    # Estereótipos de Relação
    'material': 'MATERIAL', 'derivation': 'DERIVATION', 'comparative': 'COMPARATIVE',
    'mediation': 'MEDIATION', 'characterization': 'CHARACTERIZATION',
    'externalDependence': 'EXTERNALDEPENDENCE', 'componentOf': 'COMPONENTOF', 'memberOf': 'MEMBEROF',
    'subCollectionOf': 'SUBCOLLECTIONOF', 'subQualityOf': 'SUBQUALITYOF',
    'instantiation': 'INSTANTIATION', 'termination': 'TERMINATION', 'participational': 'PARTICIPATIONAL',
    'participation': 'PARTICIPATION', 'historicalDependence': 'HISTORICALDEPENDENCE',
    'creation': 'CREATION', 'manifestation': 'MANIFESTATION', 'bringsAbout': 'BRINGSABOUT',
    'triggers': 'TRIGGERS', 'composition': 'COMPOSITION', 'aggregation': 'AGGREGATION',
    'inherence': 'INHERENCE', 'value': 'VALUE', 'formal': 'FORMAL', 'constitution': 'CONSTITUTION',

    # Meta-atributos
    'ordered': 'ORDERED', 'const': 'CONST', 'derived': 'DERIVED',
    'subsets': 'SUBSETS', 'redefines': 'REDEFINES',

    # Tipos de Dados Nativos (tratados como palavras-chave)
    'string': 'STRING_TYPE', 'number': 'NUMBER_TYPE', 'boolean': 'BOOLEAN_TYPE',
    'date': 'DATE_TYPE', 'time': 'TIME_TYPE', 'datetime': 'DATETIME_TYPE',

    # Valores Booleanos
    'true': 'BOOLEAN_VALUE', 'false': 'BOOLEAN_VALUE',
}

# Lista completa de nomes de tokens.
# É uma combinação dos símbolos que definiremos manualmente
# com todos os valores do dicionário 'reserved'.
tokens = [
    # Identificadores e Literais
    'ID', 'CLASS_NAME', 'RELATION_NAME', 'INSTANCE_NAME', 'NEW_DATATYPE',
    'NUMBER', 'STRING',

    # Símbolos Especiais
    'LBRACE', 'RBRACE', 'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET',
    'COMMA', 'COLON', 'DOTDOT', 'ASTERISK', 'AT', 'ARROW_RL', 'ARROW_LR',
] + list(reserved.values())


# -----------------------------------------------------------------------------
# 2. REGRAS PARA TOKENS SIMPLES (SÍMBOLOS)
# -----------------------------------------------------------------------------

# Expressões regulares para símbolos simples. A ordem aqui não importa.
t_LBRACE      = r'\{'
t_RBRACE      = r'\}'
t_LPAREN      = r'\('
t_RPAREN      = r'\)'
t_LBRACKET    = r'\['
t_RBRACKET    = r'\]'
t_COMMA       = r','
t_COLON       = r':'
t_DOTDOT      = r'\.\.'
t_ASTERISK    = r'\*'
t_AT          = r'@'
t_ARROW_RL    = r'<>--'
t_ARROW_LR    = r'--<>'

# Regra para ignorar espaços, tabulações. Note que removemos o '\n'.
t_ignore = ' \t'


# -----------------------------------------------------------------------------
# 3. REGRAS PARA TOKENS COMPLEXOS (COM FUNÇÕES)
# -----------------------------------------------------------------------------

# A ordem das funções importa! PLY testa as regras na ordem em que aparecem.
# Regras mais específicas devem vir antes das mais genéricas.

def t_NEW_DATATYPE(t):
    r'[a-zA-Z]+DataType'
    return t

def t_INSTANCE_NAME(t):
    r'[a-zA-Z][a-zA-Z_]*[0-9]+'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_]*'  # Removemos o 0-9 para proibir números
    t.type = reserved.get(t.value, 'ID')

    if t.type == 'ID':
        if t.value[0].isupper():
            t.type = 'CLASS_NAME'
        else:
            t.type = 'RELATION_NAME'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\"]|\\.)*\"'
    t.value = t.value[1:-1]  # Remove as aspas
    return t

def t_COMMENT(t):
    r'//.*'
    pass  # Nenhum valor de retorno, então o token é descartado

# Adicione esta função para calcular a coluna
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    # Agora podemos usar a coluna para um erro mais preciso
    col = find_column(t.lexer.lexdata, t)
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lexer.lineno}, coluna {col}")
    t.lexer.skip(1)


# -----------------------------------------------------------------------------
# 4. CONSTRUÇÃO E EXECUÇÃO DO LEXER
# -----------------------------------------------------------------------------

# Constrói o analisador léxico
lexer = lex.lex()

if __name__ == '__main__':
    data = """
    import alergiaalimentar

package alergiaalimentar

kind Paciente

kind Alimento

subkind Proteina of functional-complexes  specializes Componente_Alimentar 

phase Crianca of functional-complexes  specializes Paciente 

phase Adulto of functional-complexes  specializes Paciente 

subkind Aditivo_Alimentar of functional-complexes  specializes Componente_Alimentar 

subkind Carboidrato of functional-complexes  specializes Componente_Alimentar 

subkind Imuno_Mediada of relators  specializes Alergia 

subkind Nao_Imuno_Mediada of relators  specializes Alergia 

mode Sintoma

subkind Cutaneo of intrinsic-modes  specializes Sintoma 

subkind Gastrointestinal of intrinsic-modes  specializes Sintoma 

subkind Respiratorio of intrinsic-modes  specializes Sintoma 

subkind Sistemico of intrinsic-modes  specializes Sintoma 

role Alergeno of functional-complexes  specializes Componente_Alimentar 

relator Tratamento

relator Diagnostico

subkind Mista of relators  specializes Alergia 

kind Profissional_de_Saude

subkind Ingrediente of functional-complexes  specializes Alimento 

subkind Formula of functional-complexes  specializes Alimento 

subkind Teste_de_Dosagem_IgE_Serica of functional-complexes  specializes Procedimento 

subkind Teste_de_Provocacao_Oral of functional-complexes  specializes Procedimento 

kind Procedimento

subkind Dieta_de_Exclusao of relators  specializes Tratamento 

subkind Medicamento of relators  specializes Tratamento 

subkind Imunoterapia_Oral of relators  specializes Tratamento 

quality Comobidarde_Alergica

quality Heranca_Genetica

event Reacao_Cruzada specializes Reacao_Adversa 

relator Alergia

event Reacao_Adversa

kind Componente_Alimentar

event Consumo_Alimentar

subkind Teste_Cutaneo of functional-complexes  specializes Procedimento 

mode Disposicao_Alergica

situation Exposicao_ao_Alergeno

relator Avaliacao_de_Risco

quality Nivel_de_Risco

genset disjoint_complete {
    general Componente_Alimentar
    specifics Proteina, Aditivo_Alimentar, Carboidrato
}

genset disjoint_complete {
    general Alergia
    specifics Imuno_Mediada, Mista, Nao_Imuno_Mediada
}

genset disjoint_complete {
    general Sintoma
    specifics Respiratorio, Sistemico, Gastrointestinal, Cutaneo
}

genset disjoint_complete {
    general Procedimento
    specifics Teste_Cutaneo, Teste_de_Dosagem_IgE_Serica, Teste_de_Provocacao_Oral
}

genset disjoint_complete {
    general Alimento
    specifics Formula, Ingrediente
}

genset disjoint_complete {
    general Paciente
    specifics Crianca, Adulto
}

genset disjoint_complete {
    general Tratamento
    specifics Imunoterapia_Oral, Medicamento, Dieta_de_Exclusao
}
    """

    lexer.input(data)

    # Cria a tabela de símbolos como uma lista de dicionários
    symbol_table = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        
        # Calcula a coluna para cada token
        column = find_column(data, tok)

        symbol_table.append({
            'lexema': tok.value,
            'tipo': tok.type,
            'linha': tok.lineno,
            'coluna': column
        })

    # Imprime a tabela de forma organizada
    import json
    print(json.dumps(symbol_table, indent=4))
