"""
fisica.py
---------
Este arquivo contem SOMENTE as formulas analiticas do lancamento de
projetil (sem resistencia do ar). Nao lida com grafico nem interface.
 
Formulas usadas (conforme enunciado, Secao 2):
    x(t) = x0 + v0*cos(theta)*t
    y(t) = y0 + v0*sin(theta)*t - 0.5*g*t^2
    t_voo = (v0*sin(theta) + sqrt((v0*sin(theta))^2 + 2*g*y0)) / g
    y_max = y0 + (v0*sin(theta))^2 / (2*g)
    R     = x0 + v0*cos(theta)*t_voo
"""
 
import numpy as np
 
 
def calcular_resultados(v0, theta_graus, y0, g):
    """
    Calcula tempo de voo, altura maxima e alcance horizontal.
 
    Parametros:
        v0          -> velocidade inicial (m/s)
        theta_graus -> angulo de lancamento em GRAUS (ex: 45)
        y0          -> altura inicial (m)
        g           -> aceleracao da gravidade (m/s^2)
 
    Retorna um dicionario com t_voo, y_max e alcance (R).
    """
    theta = np.radians(theta_graus)
 
    v0x = v0 * np.cos(theta)
    v0y = v0 * np.sin(theta)
 
    t_voo = (v0y + np.sqrt(v0y**2 + 2 * g * y0)) / g
    y_max = y0 + (v0y**2) / (2 * g)
    alcance = v0x * t_voo
 
    return {
        "t_voo": t_voo,
        "y_max": y_max,
        "alcance": alcance,
    }
 
 
def calcular_trajetoria(v0, theta_graus, y0, g, x0=0, n_pontos=200):
    """
    Calcula os pontos (x, y) da trajetoria completa, do lancamento
    ate o projetil tocar o chao (y = 0).
 
    Retorna dois arrays numpy: vetor_x, vetor_y
    """
    theta = np.radians(theta_graus)
    v0x = v0 * np.cos(theta)
    v0y = v0 * np.sin(theta)
 
    resultados = calcular_resultados(v0, theta_graus, y0, g)
    t_voo = resultados["t_voo"]
 
    t = np.linspace(0, t_voo, n_pontos)
 
    x = x0 + v0x * t
    y = y0 + v0y * t - 0.5 * g * t**2
 
    return x, y
