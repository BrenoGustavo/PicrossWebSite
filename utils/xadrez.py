def criar_matriz_xadrez(linhas, colunas):
    """
    Cria uma matriz no padrão de xadrez com 1 e 0.
    
    Args:
        linhas (int): Número de linhas da matriz
        colunas (int): Número de colunas da matriz
        
    Returns:
        list: Matriz no padrão de xadrez
    """
    matriz = []
    for i in range(linhas):
        linha = []
        for j in range(colunas):
            # Alterna entre 1 e 0 baseado na soma dos índices
            # Se i+j for par, coloca 1, se for ímpar, coloca 0
            linha.append((i + j) % 2)
        matriz.append(linha)
    return matriz

# Exemplo de uso:
linhas = 5
colunas = 5
matriz_xadrez = criar_matriz_xadrez(linhas, colunas)

# Imprimindo a matriz
print(matriz_xadrez)


b = [[0 for i in range(10)] for i in range(10)]
print(b)