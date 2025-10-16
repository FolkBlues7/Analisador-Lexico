# Importa o objeto lexer e a função auxiliar do pacote lexer
from lexer.lexer import run_lexer_test

# =============================================================================
# EXEMPLOS DE ENTRADA
# =============================================================================

TEST_EXAMPLES = {
    '1': {
        'name': 'Estrutura Básica (Package, Kind, Subkind)',
        'code': """
// Exemplo 1: Estrutura Básica
package OntologiaPrincipal {
    import OutraOntologia
    
    kind EntidadeBase
    
    subkind SubEntidade of functional-complexes
    
    material hasPart
}
"""
    },
    '2': {
        'name': 'Dados, Literais e Meta-atributos',
        'code': """
// Exemplo 2: Tipos de Dados e Literais
class Pessoa {
    age: number = 42
    birthDate: date = '2025-10-15'
    isActive: boolean = true
    
    email: string ordered const
    
    CPF: CPFDataType
}
"""
    },
    '3': {
        'name': 'Relações Complexas e Identificadores',
        'code': """
// Exemplo 3: Relações Complexas
manifestation hasSymptom
    
instantiation hasInstance
    
general Pessoa specifics Aluno Professor
    
// Identificadores de exemplo
MinhaClasse
minhaRelacao
instancia1
"""
    }
}

# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================

def main():
    while True:
        print("\n" + "="*50)
        print(" SELECIONE O TESTE DE ANÁLISE LÉXICA ".center(50))
        print("="*50)
        
        # Lista as opções de teste
        for key, example in TEST_EXAMPLES.items():
            print(f" {key}. {example['name']}")
            
        print(" Q. Sair")
        print("-" * 50)
        
        # Pede a entrada do usuário
        escolha = input("Digite o número do teste (ou Q para sair): ").strip().upper()

        if escolha == 'Q':
            print("Encerrando o analisador. Até logo!")
            break
        
        if escolha in TEST_EXAMPLES:
            exemplo_selecionado = TEST_EXAMPLES[escolha]
            
            print("\n" + "#" * 50)
            print(f" Executando: {exemplo_selecionado['name']}".center(50))
            print("#" * 50)
            
            # Chama a função que executa o lexer, importada de lexer.py
            tokens_output = run_lexer_test(exemplo_selecionado['code'], exemplo_selecionado['name'])
            
            print("\n=== CÓDIGO FONTE ===")
            print(exemplo_selecionado['code'])
            print("\n=== TOKENS RECONHECIDOS ===")
            for token_line in tokens_output:
                print(token_line)
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()