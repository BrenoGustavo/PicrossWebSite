def criar_grid_com_bola(tamanho=10, raio=3):
    grid = [[0 for _ in range(tamanho)] for _ in range(tamanho)]
    centro = (tamanho - 1) / 2  # Centro do grid (considerando índices começando em 0)
      # Raio aproximado para uma bola visível em 10x10

    for i in range(tamanho):
        for j in range(tamanho):
            distancia_ao_centro = ((i - centro) ** 2 + (j - centro) ** 2) ** 0.5
            if distancia_ao_centro <= raio:
                grid[i][j] = 1

    return grid

# Cria e imprime o grid
grid = criar_grid_com_bola(10, 3)
for linha in grid:
    print(' '.join(map(str, linha)))

print('\n', grid)