# simulador-lancamento-projetil
Simulador interativo, com interface gráfica em Python, do lançamento de projéteis sem resistência do ar (caso ideal). Desenvolvido como trabalho da disciplina de Física - Práticas Extensivas.

O usuário ajusta os parâmetros do lançamento (velocidade inicial, ângulo, altura inicial e gravidade) através de sliders e vê a trajetória, os resultados numéricos e uma animação do lançamento atualizarem em tempo real.

## Funcionalidades:

 * 4 sliders interativos: velocidade inicial (v0), ângulo de lançamento (θ), altura inicial (y0) e gravidade (g)

 * Atualização do gráfico em tempo real, sem precisar reiniciar o programa

 * Exibição dos resultados numéricos: alcance horizontal, altura máxima e tempo de voo

 * Botão "Lançar" que anima o deslocamento do projétil ao longo da trajetória

 * Escala consistente entre os eixos x e y (a trajetória não aparece distorcida)

 * Tratamento de entradas inválidas (ex.: ângulo fora do intervalo, velocidade negativa)

## Como executar:

Pré-requisitos: Python 3.10 ou superior e Bibliotecas: matplotlib e numpy

 Instalação: pip install matplotlib numpy

Execução: python interface.py  - Isso abre a janela principal do simulador, com o gráfico e os controles.

## Fórmulas utilizadas:    

Com posição inicial (x0, y0), velocidade inicial v0, ângulo de lançamento θ e gravidade g:
 * Posição: x(t) = x0 + v0·cos(θ)·t e y(t) = y0 + v0·sin(θ)·t - ½·g·t²
 * Tempo de voo: t_voo = (v0·sin(θ) + √((v0·sin(θ))² + 2·g·y0)) / g
 * Altura máxima: y_max = y0 + (v0·sin(θ))² / (2·g)
 * Alcance: R = x0 + v0·cos(θ)·t_voo
