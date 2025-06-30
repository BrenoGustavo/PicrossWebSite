from django.shortcuts import render, get_object_or_404
from datetime import date
from .models import Puzzle
import json
from django.http import JsonResponse
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
        'url_verificacao': 'check_daily',
    })


def jogo_aleatorio(request):
    puzzle = utils.gerar_grid_aleatorio()
    solution = puzzle['solucao']
    size = puzzle['size']
    indices = list(range(size))
    row_hints, col_hints = utils.calcular_dicas(solution)
    rows_with_hints = list(zip(indices, row_hints))

    # Salva dicas e solução na sessão
    request.session['solucao_random'] = json.dumps(solution)
    request.session['row_hints'] = row_hints
    request.session['col_hints'] = col_hints

    return render(request, 'game/puzzle.html', {
        'size': size,
        'indices': indices,
        'solution': solution,
        'row_hints': row_hints,
        'col_hints': col_hints,
        'rows_with_hints': rows_with_hints,
        'modo': 'random',
        'url_verificacao': 'check_random',
    })


@csrf_exempt
def check_daily(request):
    if request.method != "POST":
        return JsonResponse({"erro": "Método não permitido"}, status=405)
    try:
        data = json.loads(request.body)
        resposta = data.get("resposta")

        puzzle = Puzzle.objects.get(date=date.today())
        gabarito = json.loads(puzzle.solution)

        resposta_int = [[int(c) for c in row] for row in resposta]
        gabarito_int = [[int(c) for c in row] for row in gabarito]

        return JsonResponse({"correto": resposta_int == gabarito_int})

    except Exception as e:
        print("Erro (check_daily):", e)
        return JsonResponse({"erro": "Erro interno"}, status=500)


@csrf_exempt
def check_random(request):
    if request.method != "POST":
        return JsonResponse({"erro": "Método não permitido"}, status=405)

    try:
        data = json.loads(request.body)
        resposta = data.get("resposta")

        # Converte para int
        resposta_int = [[int(cell) for cell in row] for row in resposta]

        # Calcula dicas com base na resposta do jogador
        row_resposta, col_resposta = utils.calcular_dicas(resposta_int)

        # Dicas originais
        row_hints = request.session.get("row_hints")
        col_hints = request.session.get("col_hints")

        if not row_hints or not col_hints:
            return JsonResponse({"erro": "Dicas não encontradas"}, status=400)

        correto = (row_resposta == row_hints and col_resposta == col_hints)
        return JsonResponse({"correto": correto})

    except Exception as e:
        print("Erro (check_random):", e)
        return JsonResponse({"erro": "Erro interno"}, status=500)
    

def generate_grid(request):
    size = int(request.GET.get('size', 5))  # padrão 5x5
    indices = list(range(size))
    return render(request, 'game/generate.html', {
        'size': size,
        'indices': indices,
    })