import pandas as pd

from distribuicoes import *
from relatorio_estatisticas import *
from menu import *

class Atendente:
    def __init__(self, nome):
        self.nome = nome
        self.TS_I = 0
        self.TS = 0
        self.TS_F = 0

def gera_tempos(distribuicao,qtd_valores):
    # indentifica a distribuicao
    nome_distr,parametros = list(distribuicao.items())[0]
    
    if nome_distr == "exponencial":
        media = parametros
        valores = [distribuicao_exponencial(media) for _ in range(qtd_valores)]
    
    elif nome_distr == "normal":
        media,desvio_padrao = parametros
        valores = [distribuicao_normal(media,desvio_padrao) for _ in range(qtd_valores)]
    
    elif nome_distr == "deterministico":
        valores = [parametros]*qtd_valores

    return valores

def realiza_simulacao(qtd_atendentes, tec_distr, ts_distr):
    # limite da execução da simulação
    chegadas = 10

    # tempos entre chegadas e tempos de serviço
    tec = gera_tempos(tec_distr,chegadas)
    ts = gera_tempos(ts_distr,chegadas)

    TR = TEC = TF = 0
    fila = []

    # data frame que guarda as informações da simulação
    colunas = ["Cliente","TEC","TR","Atendente","TS-I","TS","TS-F","TF"]
    simulacao = pd.DataFrame(columns=colunas)
    
    # quantidade de atendentes do sistema
    atendentes = [Atendente(i+1) for i in range(qtd_atendentes)]

    for i in range(chegadas):
        for atendente in atendentes:
            # atendente está desocupado
            if TR >= atendente.TS_F:
                atendente.TS_I = TR
                atendente_disponivel = atendente
                break
        
        # todos os atendentes estão ocupados
        else:
            # qual atendente ficará disponível primeiro
            atendente_disponivel = min(atendentes, key=lambda x: x.TS_F)
            atendente_disponivel.TS_I = atendente_disponivel.TS_F
            
            # controlar quantidade de entidades presentes na fila
            for entidade in fila:
                tempo_inicio = entidade   # quando a entidade da fila vai ser atendida
                if TR >= tempo_inicio:
                    fila.remove(tempo_inicio) 

            fila.append(atendente_disponivel.TS_I)
            
            #print(fila)

        atendente_disponivel.TS = ts.pop()
        atendente_disponivel.TS_F = atendente_disponivel.TS_I + atendente_disponivel.TS

        TF = atendente_disponivel.TS_I - TR

        simulacao.loc[i] = [round(i+1),TEC,TR,atendente_disponivel.nome,atendente_disponivel.TS_I, 
            atendente_disponivel.TS,atendente_disponivel.TS_F,TF] 
        
        TEC = tec.pop()
        TR += TEC
    
    return simulacao

def main():
    # quantidade de atendentes da simulação
    atendentes = 2

    # salvar as opções do usuário
    tec_distr = {}
    ts_distr = {}
    
    # menu que apresenta as opções
    tec_nome,tec_valor,ts_nome,ts_valor = menu()

    # distribuição do tec e ts
    tec_distr[tec_nome] = tec_valor
    ts_distr[ts_nome] = ts_valor
    
    resultado_simulacao = realiza_simulacao(atendentes,tec_distr,ts_distr)
    resultado_simulacao[["Cliente","Atendente"]] = resultado_simulacao[["Cliente","Atendente"]].astype(int)
    print(resultado_simulacao.to_string(index=False))

    print("")
    entidades_fila(resultado_simulacao)
    tempo_fila(resultado_simulacao)
    ocupacao_servidores(resultado_simulacao,atendentes)
    tempo_sistema(resultado_simulacao)
    
main()