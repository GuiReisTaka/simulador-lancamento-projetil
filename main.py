"""
main.py
-------
Como rodar:
    1. Instalar as bibliotecas (uma vez so):
       pip install matplotlib numpy
    2. Rodar:
       python main.py

Este arquivo cuida do GRAFICO e da EXECUCAO do programa.
Os calculos de fisica ficam separados em fisica.py.

Ainda NAO tem interface interativa (sliders/botoes) - isso vem
no proximo passo.
"""

import matplotlib.pyplot as plt
import numpy as np

from fisica import calcular_resultados, calcular_trajetoria


def plotar_trajetoria(v0, theta_graus, y0, g):
    """
    Recebe os parametros do lancamento, calcula tudo (usando fisica.py)
    e desenha o grafico da trajetoria com os resultados.
    """
    resultados = calcular_resultados(v0, theta_graus, y0, g)
    x, y = calcular_trajetoria(v0, theta_graus, y0, g)

    # Imprime os resultados no terminal, pra conferir os numeros
    print("----- Resultados -----")
    print(f"Tempo de voo:  {resultados['t_voo']:.2f} s")
    print(f"Altura maxima: {resultados['y_max']:.2f} m")
    print(f"Alcance:       {resultados['alcance']:.2f} m")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, y, color="royalblue", linewidth=2)

    # Marca o ponto de altura maxima e o ponto de alcance final
    ax.scatter([x[np.argmax(y)]], [resultados["y_max"]],
               color="red", zorder=5, label="Altura máxima")
    ax.scatter([x[-1]], [y[-1]],
               color="green", zorder=5, label="Ponto de queda")

    ax.set_xlabel("Distância horizontal x (m)")
    ax.set_ylabel("Altura y (m)")
    ax.set_title("Trajetória do Projétil (sem resistência do ar)")
    ax.set_aspect("equal")  # mantem escala igual entre x e y
    ax.grid(True, alpha=0.3)
    ax.legend()

    plt.show()


def main():
    # Configuracao de teste (depois isso vira controlado por sliders)
    v0 = 40          # m/s
    theta_graus = 45  # graus
    y0 = 0            # m
    g = 9.8           # m/s^2 (Terra)

    plotar_trajetoria(v0, theta_graus, y0, g)


if __name__ == "__main__":
    main()