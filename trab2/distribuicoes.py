from random import random
from math import log,cos,pi,sqrt

# método da transformação inversa
def distribuicao_exponencial(media):
    lambda_ = 1/media
    
    # valor de uma distribuição uniforme (0,1)
    u = random()   
    
    x = (-1/lambda_)*log(1-u)
    return round(x,2)

# método Box-Muller
def distribuicao_normal(media, desvio_padrao):
    # valores de uma distribuição uniforme (0,1)
    u1 = random()
    u2 = random()

    # valor de uma distribuição normal (0,1)
    z = cos(2*pi*u2)*sqrt(-2*log(u1))
    
    x = (desvio_padrao*z) + media
    return round(x,2)
