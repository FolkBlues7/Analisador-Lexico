from lexer.lexer import Lexer

def main():
    # Exemplo de entrada (arquivo TONTO)
    entrada = """
    class Person
    class Child
    relation hasParent
    instance Planeta1
    """

    lexer = Lexer()
    lexer.reserved += lexer.list(reserved.values())
    tokens = lexer.tokenize(entrada)

    print("=== Tokens Reconhecidos ===")
    for token in tokens:
        print(token)

    # Futuro: chamada ao parser (análise sintática)
    # parser = Parser(tokens)
    # arvore_sintatica = parser.parse()

    # Futuro: chamada ao verificador semântico
    # semantic_checker = SemanticAnalyzer(arvore_sintatica)
    # semantic_checker.check()

if __name__ == "__main__":
    main()

