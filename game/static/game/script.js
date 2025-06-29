let mouseDown = false;
let modo = null; // "filled" ou "marcado"
let botao = null; // 0 (esquerdo) ou 2 (direito)
let acao = null; // "adicionar" ou "remover"

document.addEventListener("DOMContentLoaded", () => {

    document.addEventListener("mousedown", e => {
        const target = e.target;
        if (!target.classList.contains('cell')) return;

        mouseDown = true;
        botao = e.button;

        if (botao === 0) {
            modo = "filled";
            acao = target.classList.contains('filled') ? "remover" : "adicionar";
        } else if (botao === 2) {
            modo = "marcado";
            acao = target.classList.contains('marcado') ? "remover" : "adicionar";
        }

        // Aplica a ação na célula inicial
        if (modo === "filled") {
            if (acao === "adicionar") {
                target.classList.add('filled');
                target.classList.remove('marcado');
            } else if (acao === "remover") {
                target.classList.remove('filled');
            }
        } else if (modo === "marcado") {
            if (acao === "adicionar") {
                if (!target.classList.contains('filled')) {
                    target.classList.add('marcado');
                }
            } else if (acao === "remover") {
                target.classList.remove('marcado');
            }
        }

        // Impede seleção de texto
        e.preventDefault();
    });
    document.addEventListener("mouseup", () => {
        mouseDown = false;
        modo = null;
        botao = null;
        acao = null;
    });

    document.querySelectorAll('.cell').forEach(c => {
        c.addEventListener('contextmenu', e => {
            e.preventDefault(); // ainda queremos impedir o menu do botão direito
        });

        c.addEventListener('mouseenter', () => {
            if (!mouseDown || !modo || !acao) return;

            if (modo === "filled") {
                if (acao === "adicionar") {
                    c.classList.add('filled');
                    c.classList.remove('marcado');
                } else if (acao === "remover") {
                    c.classList.remove('filled');
                }
            } else if (modo === "marcado") {
                if (acao === "adicionar") {
                    if (!c.classList.contains('filled')) {
                        c.classList.add('marcado');
                    }
                } else if (acao === "remover") {
                    c.classList.remove('marcado');
                }
            }
        });
    });

    function getSoluçaoDoJogador() {
    const matriz = [];

    for (let i = 0; i < tamanho; i++) {
        const linha = [];
        for (let j = 0; j < tamanho; j++) {
            const cell = document.querySelector(`.cell[data-row='${i}'][data-col='${j}']`);
            // Só conta como 1 se estiver 'filled', marcações com 'marcado' são ignoradas
            const valor = cell.classList.contains('filled') ? 1 : 0;
            linha.push(valor);
        }
        matriz.push(linha);
    }

    return matriz;
}

    window.verificar = async function () {
        const resposta = getSoluçaoDoJogador();
        const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
        
        const res = await fetch(urlVerificar, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ resposta })
        });

        const data = await res.json();
        console.log("Resposta que será enviada:", resposta);
        document.getElementById("resultado").innerText = data.correto
            ? "✅ Você acertou!"
            : "❌ Ainda não está certo.";
    };
});