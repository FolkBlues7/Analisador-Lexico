# Importa o objeto lexer do módulo lexer
from lexer.lexer import lexer 
# Importa 'os' para manipulação de caminhos de arquivo
import os
# Importa 'sys' para funções de sistema (não usado diretamente, mas boa prática)
import sys
# Importa a classe Counter para facilitar a contagem dos tokens
from collections import Counter

# =============================================================================
# EXEMPLOS DE ENTRADA
# =============================================================================

TEST_EXAMPLES = {
    '1': {
        'name': 'CarOwnershipExample',
        'code': """
// Exemplo 1: Car Ownership
package CarOwnership 

kind Organization
subkind CarAgency specializes Organization
kind Car

relator CarOwnership {
    @mediation
    -- involvesOwner -- [1] CarAgency

    @mediation
    -- involvesProperty -- [1] Car
}
"""
    },
    '2': {
        'name': 'CarRentalExample',
        'code': """
// Exemplo 2: Car Rental
package CarRental 

kind Person

role Employee specializes Person
role ResponsibleEmployee specializes Employee

phase DeceasedPerson specializes Person
phase LivingPerson specializes Person

phase Child specializes LivingPerson
phase Teenager specializes LivingPerson
phase Adult specializes LivingPerson

disjoint complete genset AgePhase {
    general LivingPerson
    specifics Child, Teenager, Adult
}

disjoint complete genset LifeStatus {
    general Person
    specifics DeceasedPerson, LivingPerson
}

roleMixin Customer

role PersonalCustomer specializes Customer, Person

kind Organization

role CorporateCustomer specializes Organization

kind Car

phase AvailableCar specializes Car
phase UnderMaintenanceCar specializes Car

role RentalCar specializes AvailableCar

relator CarRental {
    @mediation
    -- involvesRental -- [1] RentalCar
    
    -- involvesMediator -- [1] ResponsibleEmployee
    
    @mediation
    -- involvesCustomer --[1] Customer
}
"""
    },
    '3': {
        'name': 'FoodAllergyExample',
        'code': """
// Exemplo 3: Alergia Alimentar
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
    },
    '4': {
        'name': 'TDAHExample',
        'code': """
// Exemplo 4: TDAH
import TDAH

package TDAH

category Hyperactivity_Symptom

category Neurologically_Based_Condition specializes Medical_Condition 

mixin Medical_Condition 

category Inattention_Symptom 

role Patient specializes Person 

relator Medical_Report

role Doctor specializes Person 

kind Person

mode Behavioral_Therapy

mode Medication_Therapy

subkind Methylphenidate_ specializes Medicine 

subkind Dextroamphetamine_ specializes Medicine 

relator Prescription

phase Preschool_Age specializes Patient 

phase School_Age specializes Patient 

phase Teenager specializes Patient 

phase Adult specializes Patient 

quality Birth_Sex

kind Medicine

role Psychologist specializes Person 

kind Criterion_B

kind Criterion_C

kind Criterion_D

kind Criterion_E

kind Criterion_A1a specializes Hyperactivity_Symptom 

kind Criterion_A1b specializes Hyperactivity_Symptom 

kind Criterion_A1c specializes Hyperactivity_Symptom 

kind Criterion_A1d specializes Hyperactivity_Symptom 

kind Criterion_A1e specializes Hyperactivity_Symptom 

kind Criterion_A1f specializes Hyperactivity_Symptom 

kind Criterion_A1g specializes Hyperactivity_Symptom 

kind Criterion_A1h specializes Hyperactivity_Symptom 

kind Criterion_A1i specializes Hyperactivity_Symptom 

kind Criterion_A2a specializes Inattention_Symptom 

kind Criterion_A2b specializes Inattention_Symptom 

kind Criterion_A2c specializes Inattention_Symptom 

kind Criterion_A2d specializes Inattention_Symptom 

kind Criterion_A2e specializes Inattention_Symptom 

kind Criterion_A2f specializes Inattention_Symptom 

kind Criterion_A2g specializes Inattention_Symptom 

kind Criterion_A2h specializes Inattention_Symptom 

kind Criterion_A2i specializes Inattention_Symptom 

quality Severity

subkind Criterion_A1 specializes Criterion_A 

subkind Criterion_A2 specializes Criterion_A 

kind Criterion_A

kind ADHD specializes Neurologically_Based_Condition 

disjoint complete genset TypesOfMedicine {
    general Medicine
    specifics Dextroamphetamine_, Methylphenidate_
}

disjoint complete genset PhasesOfAPatient{
    general Patient
    specifics Preschool_Age, School_Age, Adult, Teenager
}
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
            
        print(" 5. Testar Arquivo Externo (.tonto)")
        print(" Q. Sair")
        print("-" * 50)
        
        # Pede a entrada do usuário
        escolha = input("Digite o número do teste (ou Q para sair): ").strip().upper()

        if escolha == 'Q':
            print("Encerrando o analisador. Até logo!")
            break
            
        codigo_para_analise = ""
        nome_do_teste = ""

        if escolha in TEST_EXAMPLES:
            exemplo_selecionado = TEST_EXAMPLES[escolha]
            codigo_para_analise = exemplo_selecionado['code']
            nome_do_teste = exemplo_selecionado['name']
            
        elif escolha == '5':
            print("\n--- INSTRUÇÕES PARA ARQUIVO EXTERNO ---")
            print("1. Coloque o arquivo .tonto em um local acessível.")
            print("2. Digite o caminho completo do arquivo (ex: 'C:\\Users\\SeuUsuario\\Desktop\\meu_teste.tonto').")
            print("---------------------------------------")
            file_path = input("Digite o caminho do arquivo .tonto: ").strip()
            
            # 1. Verificar se o arquivo existe
            if not os.path.exists(file_path):
                print(f"\n[ERRO] Arquivo não encontrado no caminho: {file_path}")
                print("Por favor, verifique o nome ou o caminho e tente novamente.")
                continue # Volta ao menu principal
            
            # 2. Ler o conteúdo do arquivo
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    codigo_para_analise = f.read()
                nome_do_teste = f"Arquivo Externo: {os.path.basename(file_path)}"
            except Exception as e:
                print(f"\n[ERRO] Não foi possível ler o arquivo: {e}")
                continue # Volta ao menu principal
                
        else:
            print("Opção inválida. Tente novamente.")
            continue # Volta ao menu principal

        # --- PARTE DE EXECUÇÃO DO LEXER (UNIFICADA) ---
        print("\n" + "#" * 50)
        print(f" Executando: {nome_do_teste}".center(50))
        print("#" * 50)
        
        print("\n=== CÓDIGO FONTE ANALISADO ===")
        print(codigo_para_analise)
        print("---------------------------------")
        
        # << INÍCIO DA NOVA LÓGICA >>
        
        # 1. Inicializa um contador para os tipos de token
        token_counts = Counter()

        # 2. Fornece o código ao lexer
        lexer.input(codigo_para_analise)

        print("\n=== VISÃO ANALÍTICA (LISTA DE TOKENS) ===")
        # 3. Itera sobre todos os tokens encontrados
        while True:
            token = lexer.token()
            if not token:
                break  # Fim da análise
            
            # Imprime o token encontrado (Visão Analítica)
            print(f"  [Tipo: {token.type:<20} Lexema: '{token.value}' Linha: {token.lineno}]")
            
            # Atualiza a contagem para o tipo do token atual
            token_counts[token.type] += 1
            
        # 4. Seção para imprimir a Tabela de Síntese
        print("\n" + "="*50)
        print("=== TABELA DE SÍNTESE (CONTAGEM DE TOKENS) ===".center(50))
        print("="*50)

        if not token_counts:
            print("Nenhum token foi encontrado.")
        else:
            # Ordena os itens por nome do token para uma exibição consistente
            for token_type, count in sorted(token_counts.items()):
                print(f"  {token_type:<25}: {count}")
        # << FIM DA NOVA LÓGICA >>

if __name__ == "__main__":
    main()