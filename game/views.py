from django.shortcuts import render, get_object_or_404
from datetime import date
from .models import Puzzle
import json
from django.http import HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from utils import utils


def daily_puzzle(request):
    today = date.today()
    puzzle = get_object_or_404(Puzzle, date=today)
    solution = json.loads(puzzle.solution)
    size = puzzle.size
    indices = list(range(size))
    row_hints, col_hints = utils.calcular_dicas(solution)
    rows_with_hints = list(zip(indices, row_hints))

    return render(request, 'game/puzzle.html', {
        'size': size,
        'indices': indices,
        'solution': solution,
        'row_hints': row_hints,
        'col_hints': col_hints,
        'rows_with_hints': rows_with_hints,
        'modo': 'daily',
    })


def jogo_aleatorio(request):
    puzzle = utils.gerar_grid_aleatorio()
    solution = puzzle['solucao']
    size = len(solution)
    indices = list(range(size))
    row_hints, col_hints = utils.calcular_dicas(solution)
    rows_with_hints = list(zip(indices, row_hints))

    request.session["solucao_aleatoria"] = json.dumps(solution)

    return render(request, 'game/puzzle.html', {
        'size': size,
        'indices': indices,
        # 'solution': solution,
        'row_hints': row_hints,
        'col_hints': col_hints,
        'rows_with_hints': rows_with_hints,
        'modo': 'random',
    })


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from datetime import date
from .models import Puzzle

@csrf_exempt
def check_solution(request):
    if request.method != "POST":
        return JsonResponse({"erro": "Método não permitido"}, status=405)

    try:
        data = json.loads(request.body)
        resposta = data.get("resposta")

        print("🔍 Resposta recebida do frontend:", resposta)

        if not isinstance(resposta, list):
            return JsonResponse({"erro": "Formato inválido da resposta"}, status=400)

        # Converte cada célula para inteiro com validação
        resposta_int = []
        for i, row in enumerate(resposta):
            nova_linha = []
            for j, cell in enumerate(row):
                if str(cell).strip() not in ("0", "1"):
                    raise ValueError(f"Valor inválido na célula ({i},{j}): {cell}")
                nova_linha.append(int(cell))
            resposta_int.append(nova_linha)

        # Verifica se é puzzle aleatório (da sessão)
        gabarito_str = request.session.pop("solucao_aleatoria", None)

        if gabarito_str:
            print("🧪 Comparando com puzzle aleatório")
            gabarito = json.loads(gabarito_str)
        else:
            print("📅 Comparando com puzzle diário")
            puzzle = Puzzle.objects.get(date=date.today())
            gabarito = json.loads(puzzle.solution)

        print("✅ Gabarito:", gabarito)
        gabarito_int = [[int(cell) for cell in row] for row in gabarito]

        correto = resposta_int == gabarito_int
        return JsonResponse({"correto": correto})

    except Exception as e:
        print("❌ Erro na verificação:", str(e))
        return JsonResponse({"erro": "Erro interno no servidor"}, status=500)
