"""
interface.py
------------
Como rodar:
    1. Instalar as bibliotecas (uma vez so):
       pip install matplotlib numpy
    2. Rodar:
       python interface.py

Este arquivo cuida da INTERFACE GRAFICA (sliders, botao, texto de
resultados). Toda a fisica (calculos) fica em fisica.py - este
arquivo so CHAMA as funcoes de la, nunca refaz contas de fisica aqui.

Logica geral de atualizacao:
    1. Usuario mexe em um slider (ex: velocidade)
    2. O matplotlib chama automaticamente a funcao 'atualizar()'
    3. 'atualizar()' pega os valores atuais de TODOS os sliders
    4. Chama fisica.calcular_resultados() e fisica.calcular_trajetoria()
    5. Redesenha a linha da trajetoria e o texto dos resultados
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

from fisica import calcular_resultados, calcular_trajetoria


# ---------------------------------------------------------------
# CONFIGURACAO INICIAL DA JANELA
# ---------------------------------------------------------------

# Valores iniciais (o que aparece quando o programa abre)
V0_INICIAL = 40
THETA_INICIAL = 45
Y0_INICIAL = 0
G_INICIAL = 9.8

fig, ax = plt.subplots(figsize=(9, 7))
# Deixa espaco embaixo do grafico para caber os sliders e o botao
plt.subplots_adjust(left=0.1, bottom=0.42)

# Linha da trajetoria (comeca vazia, e preenchida em atualizar())
linha_trajetoria, = ax.plot([], [], color="royalblue", linewidth=2)

# Pontos de destaque: altura maxima e ponto de queda
ponto_altura_max = ax.scatter([], [], color="red", zorder=5, label="Altura máxima")
ponto_queda = ax.scatter([], [], color="green", zorder=5, label="Ponto de queda")

# Ponto do projetil que sera animado pelo botao "Lançar"
ponto_projetil, = ax.plot([], [], "o", color="black", markersize=8, zorder=6)

ax.set_xlabel("Distância horizontal x (m)")
ax.set_ylabel("Altura y (m)")
ax.set_title("Trajetória do Projétil (sem resistência do ar)")
ax.grid(True, alpha=0.3)
ax.legend(loc="upper right")

# Texto com os resultados numericos, mostrado no canto do grafico
texto_resultados = ax.text(
    0.02, 0.95, "", transform=ax.transAxes,
    verticalalignment="top", fontsize=10,
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
)

# Texto de aviso de erro (entrada invalida). Comeca escondido.
texto_erro = ax.text(
    0.5, 0.5, "", transform=ax.transAxes,
    ha="center", va="center", fontsize=12, color="red",
    bbox=dict(boxstyle="round", facecolor="mistyrose")
)
texto_erro.set_visible(False)


# ---------------------------------------------------------------
# CRIACAO DOS SLIDERS
# ---------------------------------------------------------------
# Cada slider precisa de um "eixo" (posicao/tamanho na janela) proprio.
# [esquerda, baixo, largura, altura] em fracao da figura (0 a 1)

eixo_v0 = plt.axes([0.15, 0.30, 0.7, 0.03])
slider_v0 = Slider(eixo_v0, "v0 (m/s)", 5, 150, valinit=V0_INICIAL)

eixo_theta = plt.axes([0.15, 0.25, 0.7, 0.03])
slider_theta = Slider(eixo_theta, "θ (graus)", 1, 89, valinit=THETA_INICIAL)

eixo_y0 = plt.axes([0.15, 0.20, 0.7, 0.03])
slider_y0 = Slider(eixo_y0, "y0 (m)", 0, 50, valinit=Y0_INICIAL)

eixo_g = plt.axes([0.15, 0.15, 0.7, 0.03])
slider_g = Slider(eixo_g, "g (m/s²)", 1.6, 24.8, valinit=G_INICIAL)

# Botao para lancar a animacao
eixo_botao = plt.axes([0.4, 0.05, 0.2, 0.05])
botao_lancar = Button(eixo_botao, "Lançar")


# ---------------------------------------------------------------
# FUNCAO DE ATUALIZACAO (o coracao da interface)
# ---------------------------------------------------------------

# Contador que muda toda vez que algum slider e mexido. Usado para
# a animacao do botao "Lançar" saber se os parametros mudaram
# NO MEIO do lancamento (e, se sim, cancelar a animacao antiga em
# vez de continuar seguindo uma trajetoria que ja nao existe mais).
versao_parametros = 0


def atualizar(val=None):
    """
    Chamada automaticamente pelo matplotlib toda vez que QUALQUER
    slider e mexido (val=None quando chamamos manualmente).

    Le os valores atuais dos sliders, pede pra fisica.py calcular
    tudo de novo, e redesenha o grafico.
    """
    global versao_parametros
    versao_parametros += 1  # avisa a animacao (se estiver rodando) que mudou algo

    v0 = slider_v0.val
    theta_graus = slider_theta.val
    y0 = slider_y0.val
    g = slider_g.val

    # --------- Tratamento de entradas invalidas ---------
    # Os sliders ja limitam o range (ex: v0 nunca fica negativo),
    # mas deixamos essa checagem explicita, como pede o enunciado,
    # para o caso de o codigo ser adaptado depois para caixas de
    # texto (onde o usuario PODE digitar qualquer coisa).
    if v0 <= 0 or not (0 < theta_graus < 90) or g <= 0:
        texto_erro.set_text("Entrada inválida: v0 e g devem ser > 0,\n"
                             "e o ângulo deve estar entre 0° e 90°.")
        texto_erro.set_visible(True)
        linha_trajetoria.set_data([], [])
        fig.canvas.draw_idle()
        return
    else:
        texto_erro.set_visible(False)

    # --------- Calculos (delegados ao fisica.py) ---------
    resultados = calcular_resultados(v0, theta_graus, y0, g)
    x, y = calcular_trajetoria(v0, theta_graus, y0, g)

    # --------- Atualiza o desenho ---------
    linha_trajetoria.set_data(x, y)

    idx_max = np.argmax(y)
    ponto_altura_max.set_offsets([[x[idx_max], resultados["y_max"]]])
    ponto_queda.set_offsets([[x[-1], y[-1]]])

    # Reajusta os limites do grafico para a nova trajetoria caber bem
    ax.set_xlim(min(0, x.min()) - 5, x.max() * 1.1 + 5)
    ax.set_ylim(min(0, y.min()) - 5, max(y.max(), resultados["y_max"]) * 1.2 + 5)
    ax.set_aspect("auto")  # 'equal' pode ficar estranho com ranges dinamicos

    # Atualiza o texto com os resultados numericos
    texto_resultados.set_text(
        f"Tempo de voo:  {resultados['t_voo']:.2f} s\n"
        f"Altura máxima: {resultados['y_max']:.2f} m\n"
        f"Alcance:       {resultados['alcance']:.2f} m"
    )

    fig.canvas.draw_idle()


# Conecta cada slider a funcao de atualizacao: sempre que o valor
# muda, 'atualizar' e chamada automaticamente pelo matplotlib.
slider_v0.on_changed(atualizar)
slider_theta.on_changed(atualizar)
slider_y0.on_changed(atualizar)
slider_g.on_changed(atualizar)


# ---------------------------------------------------------------
# ANIMACAO DO LANCAMENTO (botao "Lançar")
# ---------------------------------------------------------------

def lancar(event):
    """
    Chamada quando o usuario clica no botao "Lançar".
    Anima um ponto preto se movendo ao longo da trajetoria JA
    calculada (nao recalcula nada, so percorre os pontos x, y
    que ja estao desenhados na linha).

    Se o usuario mexer em algum slider NO MEIO da animacao, o
    lancamento atual e cancelado (em vez de continuar seguindo uma
    trajetoria que ja nao corresponde mais aos sliders atuais).
    """
    v0 = slider_v0.val
    theta_graus = slider_theta.val
    y0 = slider_y0.val
    g = slider_g.val

    if v0 <= 0 or not (0 < theta_graus < 90) or g <= 0:
        return  # nao anima se a configuracao atual for invalida

    x, y = calcular_trajetoria(v0, theta_graus, y0, g, n_pontos=60)

    # Guarda a "versao" dos parametros no instante do clique.
    # Se essa versao mudar durante o loop, sabemos que algum
    # slider foi mexido e cancelamos a animacao.
    minha_versao = versao_parametros

    for i in range(len(x)):
        if versao_parametros != minha_versao:
            break  # usuario mudou algum slider: cancela essa animacao

        ponto_projetil.set_data([x[i]], [y[i]])
        fig.canvas.draw_idle()
        plt.pause(0.02)  # pequena pausa entre cada quadro da animacao

    # Some com o ponto no final (ou no cancelamento) da animacao
    ponto_projetil.set_data([], [])
    fig.canvas.draw_idle()


botao_lancar.on_clicked(lancar)


# ---------------------------------------------------------------
# EXECUCAO
# ---------------------------------------------------------------

if __name__ == "__main__":
    atualizar()  # desenha a trajetoria inicial antes de qualquer interacao
    plt.show()