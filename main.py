# Importa o objeto lexer do módulo lexer
from lexer.lexer import lexer
# Importa 'os' para manipulação de caminhos de arquivo
import os
# Importa 'sys' para funções de sistema (não usado diretamente, mas boa prática)
import sys
# Importa a classe Counter para facilitar a contagem dos tokens
from collections import Counter
# Importa o módulo JSON para formatar a AST
import json 

# Importa o analisador sintático (CERTIFIQUE-SE DE QUE ESTE CAMINHO ESTÁ CORRETO)
# Assumindo que este import existe para as funções auxiliares
from parser.parser import parse_tonto_code 

# =============================================================================
# EXEMPLOS DE ENTRADA (MANTIDOS)
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
# FUNÇÕES DE ANÁLISE (AUXILIARES - MANTIDAS)
# =============================================================================

def executar_analise_lexica(codigo_para_analise, nome_do_teste):
    """Executa a análise léxica."""
    print("\n" + "#" * 50)
    print(f" EXECUTANDO ANÁLISE LÉXICA: {nome_do_teste}".center(50))
    print("#" * 50)
    
    token_counts = Counter()
    lexer.lineno = 1 
    lexer.input(codigo_para_analise)

    print("\n=== VISÃO ANALÍTICA (LISTA DE TOKENS) ===")
    while True:
        token = lexer.token()
        if not token:
            break
        print(f"  [Tipo: {token.type:<20} Lexema: '{token.value}' Linha: {token.lineno}]")
        token_counts[token.type] += 1
        
    print("\n" + "="*50)
    print("=== TABELA DE SÍNTESE (CONTAGEM DE TOKENS) ===".center(50))
    print("="*50)

    if not token_counts:
        print("Nenhum token foi encontrado.")
    else:
        for token_type, count in sorted(token_counts.items()):
            print(f"  {token_type:<25}: {count}")

def executar_analise_sintatica(codigo_para_analise, nome_do_teste):
    """Executa a análise sintática do código usando o parser PLY."""
    
    print("\n" + "#" * 50)
    print(f" EXECUTANDO ANÁLISE SINTÁTICA: {nome_do_teste}".center(50))
    print("#" * 50)
    
    try:
        # Chama a função principal de parse do seu parser.py
        resultado_ast = parse_tonto_code(codigo_para_analise)
        
        if resultado_ast is not None:
            print("\n[SUCESSO] Código aceito pela gramática (até o momento)!")
            print("\n=== ÁRVORE DE SINTAXE ABSTRATA (AST) ===")
            print(json.dumps(resultado_ast, indent=4, ensure_ascii=False)) 
        else:
            print("\n[FALHA SINTÁTICA] O parser rejeitou o código. Verifique as mensagens de erro.")
            
    except Exception as e:
        print(f"\n[ERRO INESPERADO DO PARSER] Falha na execução: {e}")

# =============================================================================
# FUNÇÃO PRINCIPAL (FLUXO INVERTIDO E CORRIGIDO)
# =============================================================================

def main():
    while True:
        # ====================================================
        # 1. ESCOLHA DO TIPO DE ANÁLISE (PRIMEIRO PASSO)
        # ====================================================
        print("\n" + "="*50)
        print(" 1. SELECIONE O TIPO DE ANÁLISE ".center(50))
        print("="*50)
        print(" 1. Análise Léxica")
        print(" 2. Análise Sintática")
        print(" 3. Análise Semântica (Em desenvolvimento)")
        print(" Q. Sair")
        print("-" * 50)

        tipo_analise = input("Digite sua escolha: ").strip().upper()

        if tipo_analise == 'Q':
            print("Encerrando o analisador. Até logo!")
            break

        if tipo_analise not in ['1', '2', '3']:
            print("Opção inválida. Tente novamente.")
            continue
            
        # Variável para armazenar a função a ser executada
        funcao_analise = None
        
        if tipo_analise == '1':
            funcao_analise = executar_analise_lexica
        elif tipo_analise == '2':
            funcao_analise = executar_analise_sintatica
        elif tipo_analise == '3':
            print("\n[INFO] Análise Semântica selecionada. Esta funcionalidade está em desenvolvimento e será tratada como placeholder.")
            # Definir uma função placeholder para Semântica se necessário, ou prosseguir

        # ====================================================
        # 2. ESCOLHA DO CÓDIGO FONTE (SEGUNDO PASSO)
        # ====================================================

        while True:
            print("\n" + "="*50)
            print(f" 2. SELECIONE O CÓDIGO FONTE para '{tipo_analise}'".center(50))
            print("="*50)
            
            # Lista as opções de teste
            for key, example in TEST_EXAMPLES.items():
                print(f" {key}. {example['name']}")
                
            print(" 5. Testar Arquivo Externo (.tonto)")
            print(" B. Voltar ao menu de Análise")
            print("-" * 50)
            
            escolha_codigo = input("Digite o número do teste (ou B para Voltar): ").strip().upper()

            if escolha_codigo == 'B':
                break # Volta ao menu principal (Seleção de Tipo de Análise)
            
            codigo_para_analise = ""
            nome_do_teste = ""

            # A. CARREGAR O CÓDIGO FONTE
            if escolha_codigo in TEST_EXAMPLES:
                exemplo_selecionado = TEST_EXAMPLES[escolha_codigo]
                codigo_para_analise = exemplo_selecionado['code']
                nome_do_teste = exemplo_selecionado['name']
                
            elif escolha_codigo == '5': 
                print("\n--- INSTRUÇÕES PARA ARQUIVO EXTERNO ---")
                print("1. Coloque o arquivo .tonto em um local acessível.")
                print("2. Digite o caminho completo do arquivo.")
                print("---------------------------------------")
                file_path = input("Digite o caminho do arquivo .tonto: ").strip()
                
                if not os.path.exists(file_path):
                    print(f"\n[ERRO] Arquivo não encontrado no caminho: {file_path}")
                    continue 
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        codigo_para_analise = f.read()
                    nome_do_teste = f"Arquivo Externo: {os.path.basename(file_path)}"
                except Exception as e:
                    print(f"\n[ERRO] Não foi possível ler o arquivo: {e}")
                    continue 
                    
            else: 
                print("Opção inválida. Tente novamente.")
                continue 
            
            # ====================================================
            # 3 & 4. EXECUTAR ANÁLISE
            # ====================================================
            
            print("\n=== CÓDIGO FONTE CARREGADO ===")
            print(codigo_para_analise)
            print("---------------------------------")

            if funcao_analise:
                funcao_analise(codigo_para_analise, nome_do_teste)
            else: # Caso Semântica (3) tenha sido selecionada, e não haja função
                print(f"\n[RESULTADO] Análise Semântica para '{nome_do_teste}' concluída (placeholder).")

            input("\nPressione ENTER para continuar...")
            break # Volta ao menu principal (Seleção de Tipo de Análise)


if __name__ == "__main__":
    main()