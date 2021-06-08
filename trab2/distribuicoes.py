from random import random
from math import log,cos,pi,sqrt

# método da transformação inversa
def distribuicao_exponencial(lambd):
    # valor de uma distribuição uniforme (0,1)
    u = random()   
    
    x = (-1/lambd)*log(1-u)
    return x

# método Box-Muller
def distribuicao_normal(media, desvio_padrao):
    # valores de uma distribuição uniforme (0,1)
    u1 = random()
    u2 = random()

    # valor de uma distribuição normal (0,1)
    z = cos(2*pi*u2)*sqrt(-2*log(u1))
    
    x = (desvio_padrao*z) + media
    return x
