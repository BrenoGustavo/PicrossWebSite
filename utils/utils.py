
import random
from datetime import date

def calcular_dicas(matriz):
    def contar_blocos(linha):
        blocos = []
        count = 0
        for val in linha:
            if val == 1:
                count += 1
            else:
                if count > 0:
                    blocos.append(count)
                    count = 0
        if count > 0:
            blocos.append(count)
        return blocos or [0]

    # Dicas por linha
    row_hints = [contar_blocos(linha) for linha in matriz]

    # Dicas por coluna (transposta)
    colunas = list(zip(*matriz))  # transpor
    col_hints = [contar_blocos(col) for col in colunas]

    return row_hints, col_hints


def gerar_grid_aleatorio(size=5):
    grid = [[random.choice([0, 1]) for _ in range(size)] for _ in range(size)]
    # gerar dicas de linha e coluna aqui

    row_hints, col_hints = calcular_dicas(grid)
    return {
        'size': size,
        'rows_with_hints': list(enumerate(row_hints)),
        'col_hints': col_hints,
        'solucao': grid
    }