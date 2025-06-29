from django.shortcuts import render, get_object_or_404
from datetime import date
from .models import Puzzle
import json
from django.http import HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt

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

def daily_puzzle(request):
    today = date.today()
    puzzle = get_object_or_404(Puzzle, date=today)
    solution = json.loads(puzzle.solution)
    size = puzzle.size
    indices = list(range(size))
    row_hints, col_hints = calcular_dicas(solution)
    rows_with_hints = list(zip(indices, row_hints))

    return render(request, 'game/puzzle.html', {
        'size': size,
        'indices': indices,
        'solution': solution,
        'row_hints': row_hints,
        'col_hints': col_hints,
        'rows_with_hints': rows_with_hints,
    })

@csrf_exempt
def check_solution(request):
    if request.method == "POST":
        data = json.loads(request.body)
        resposta = data.get("resposta")

        try:
            puzzle = Puzzle.objects.get(date=date.today())
            gabarito = json.loads(puzzle.solution)
        except Puzzle.DoesNotExist:
            return JsonResponse({"erro": "Puzzle do dia não encontrado"}, status=404)

        # Transforma ambas em matrizes de inteiros
        resposta_int = [[int(cell) for cell in row] for row in resposta]
        gabarito_int = [[int(cell) for cell in row] for row in gabarito]

        correto = resposta_int == gabarito_int
        return JsonResponse({"correto": correto})

    return JsonResponse({"erro": "Método não permitido"}, status=405)