# Acessa o objeto 'lexer' dentro do arquivo 'lexer.py' no pacote 'lexer'
from ..lexer.lexer import lexer 
# Acessa o dicionário 'tokens' e 'reserved' do arquivo 'tokens.py' no pacote 'lexer'
from ..lexer.tokens import tokens 
# (Note os dois pontos '..' para subir um nível e entrar no pacote 'lexer')

# Função auxiliar para processar um bloco de código
def run_lexer_test(code_example, test_name):
    print("=" * 50)
    print(f"--- INÍCIO DO TESTE: {test_name} ---")
    print("=" * 50)
    
    # Reseta o lexer
    lexer.input(code_example)
    
    # Processa e imprime os tokens
    while True:
        tok = lexer.token()
        if not tok:
            break
        # Usamos apenas tok.lineno pois find_column foi removida do lexer.py
        print(f"Tipo: {tok.type:<25} | Lexema: '{str(tok.value):<20}' | Linha: {tok.lineno}")
        
    print("-" * 50)
    print(f"--- FIM DO TESTE: {test_name} ---")
    print("\n\n")


# =============================================================================
# EXEMPLOS DE TESTE
# =============================================================================

# Exemplo 1: Estrutura Básica de Pacote, Classe e Relação
def test_example_1_basic_structure():
    code = """
// Exemplo 1: Estrutura Básica
package OntologiaPrincipal {
    import OutraOntologia
    
    kind EntidadeBase
    
    subkind SubEntidade of functional-complexes
    
    material hasPart
}
"""
    run_lexer_test(code, "Estrutura Básica (Package, Kind, Subkind)")


# Exemplo 2: Tipos de Dados, Literais e Meta-atributos
def test_example_2_data_and_attributes():
    code = """
// Exemplo 2: Tipos de Dados e Literais
class Pessoa {
    age: number = 42
    birthDate: date = '2025-10-15'
    isActive: boolean = true
    
    email: string ordered const
    
    CPF: CPFDataType
}
"""
    run_lexer_test(code, "Dados, Literais e Meta-atributos")


# Exemplo 3: Relações Complexas e Identificadores
def test_example_3_complex_relations():
    code = """
// Exemplo 3: Relações Complexas
manifestation hasSymptom
    
instantiation hasInstance
    
general Pessoa specifics Aluno Professor
    
// Identificadores de exemplo
MinhaClasse
minhaRelacao
instancia1
"""
    run_lexer_test(code, "Relações e Identificadores")


# =============================================================================
# EXECUÇÃO DOS TESTES
# =============================================================================

if __name__ == '__main__':
    test_example_1_basic_structure()
    test_example_2_data_and_attributes()
    test_example_3_complex_relations()