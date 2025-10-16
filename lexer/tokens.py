# =============================================================================
# 1. LISTA DE TOKENS VÁLIDOS (TODOS EM MAIÚSCULO)
# =============================================================================

tokens = [

    # Estereótipos de classe:
    'EVENT', 'SITUATION', 'PROCESS', 'CATEGORY', 'MIXIN',
    'PHASEMIXIN', 'ROLEMIXIN', 'HISTORICALROLEMIXIN', 'KIND', 'COLLECTIVE',
    'QUANTITY', 'QUALITY', 'MODE', 'INTRISICMODE', 'EXTRINSICMODE', 'SUBKIND',
    'PHASE', 'ROLE', 'HISTORICALROLE',

    # Estereótipos de relações:
    'MATERIAL', 'DERIVATION', 'COMPARATIVE', 'MEDIATION',
    'CHARACTERIZATION', 'EXTERNALDEPENDENCE', 'COMPONENTOF', 'MEMBEROF',
    'SUBCOLLECTIONOF', 'SUBQUALITYOF', 'INSTANTIATION', 'TERMINATION',
    'PARTICIPATIONAL', 'PARTICIPATION', 'HISTORICALDEPENDENCE', 'CREATION',
    'MANIFESTATION', 'BRINGSABOUT', 'TRIGGERS', 'COMPOSITION', 'AGGREGATION',
    'INHERENCE', 'VALUE', 'FORMAL', 'CONSTITUTION',

    # Palavras reservadas:
    'GENSET', 'DISJOINT', 'COMPLETE', 'GENERAL', 'SPECIFICS', 'WHERE', 'PACKAGE', 'IMPORT', 'FUNCTIONALCOMPLEXES', 'CLASS',

    # Símbolos especiais:
    'LBRACE', 'RBRACE', 'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET',
    'DOTDOT', 'ARROW_RL', 'ARROW_LR', 'ASTERISK', 'AT', 'COLON',

    # Nomes/Convenções (Identificadores):
    'CLASS_NAME',      # Nome de Classes (Começa com Maiúscula)
    'RELATION_NAME',   # Nome de Relações (Começa com Minúscula)
    'INSTANCE_NAME',   # Nome de Instâncias (Termina com Número)
    'NEW_DATATYPE',    # Novos Tipos de Dados (Ex: CPFDataType)

    # Tipos de dados nativos:
    'NUMBER_TYPE',
    'STRING_TYPE',
    'BOOLEAN_TYPE',
    'DATE_TYPE',
    'TIME_TYPE',
    'DATETIME_TYPE',

    # Valores Literais:
    'NUMBER',
    'STRING',
    'BOOLEAN_VALUE',
    'DATE_LITERAL',
    'TIME_LITERAL',
    'DATETIME_LITERAL',
    
    # Meta-atributos:
    'ORDERED', 'CONST', 'DERIVED', 'SUBSETS', 'REDEFINES',
]

# =============================================================================
# 2. MAPA DE PALAVRAS RESERVADAS (reserved)
# =============================================================================

reserved = {
    # Estereótipos de classe:
    'event': 'EVENT', 'situation': 'SITUATION', 'process': 'PROCESS', 'category': 'CATEGORY',
    'mixin': 'MIXIN', 'phaseMixin': 'PHASEMIXIN', 'roleMixin': 'ROLEMIXIN',
    'historicalRoleMixin': 'HISTORICALROLEMIXIN', 'kind': 'KIND', 'collective': 'COLLECTIVE',
    'quantity': 'QUANTITY', 'quality': 'QUALITY', 'mode': 'MODE', 'intrisicMode': 'INTRISICMODE',
    'extrinsicMode': 'EXTRINSICMODE', 'subkind': 'SUBKIND', 'phase': 'PHASE',
    'role': 'ROLE', 'historicalRole': 'HISTORICALROLE',

    # Estereótipos de relações:
    'material': 'MATERIAL', 'derivation': 'DERIVATION', 'comparative': 'COMPARATIVE',
    'mediation': 'MEDIATION', 'characterization': 'CHARACTERIZATION',
    'externalDependence': 'EXTERNALDEPENDENCE', 'componentOf': 'COMPONENTOF',
    'memberOf': 'MEMBEROF', 'subCollectionOf': 'SUBCOLLECTIONOF',
    'subQualityOf': 'SUBQUALITYOF', 'instantiation': 'INSTANTIATION',
    'termination': 'TERMINATION', 'participational': 'PARTICIPATIONAL',
    'participation': 'PARTICIPATION', 'historicalDependence': 'HISTORICALDEPENDENCE',
    'creation': 'CREATION', 'manifestation': 'MANIFESTATION', 'bringsAbout': 'BRINGSABOUT',
    'triggers': 'TRIGGERS', 'composition': 'COMPOSITION', 'aggregation': 'AGGREGATION',
    'inherence': 'INHERENCE', 'value': 'VALUE', 'formal': 'FORMAL', 'constitution': 'CONSTITUTION',

    # Palavras reservadas (Comandos de estrutura):
    'genset': 'GENSET', 'disjoint': 'DISJOINT', 'complete': 'COMPLETE',
    'general': 'GENERAL', 'specifics': 'SPECIFICS', 'where': 'WHERE',
    'package': 'PACKAGE', 'class': 'CLASS', 'import': 'IMPORT',
    'functional-complexes': 'FUNCTIONALCOMPLEXES',

    # Tipos de dados primitivos:
    'number': 'NUMBER_TYPE', 'string': 'STRING_TYPE', 'boolean': 'BOOLEAN_TYPE',
    'date': 'DATE_TYPE', 'time': 'TIME_TYPE', 'datetime': 'DATETIME_TYPE',

    # Valores booleanos:
    'true': 'BOOLEAN_VALUE',
    'false': 'BOOLEAN_VALUE',

    # Meta atributos:
    'ordered': 'ORDERED', 'const': 'CONST', 'derived': 'DERIVED',
    'subsets': 'SUBSETS', 'redefines': 'REDEFINES',
}
