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

def realiza_simulacao(qtd_atendentes, tec_distr, ts_distr, limite_fila):
    # limite da execução da simulação
    limite_simulacao = 10
    chegadas = 0

    # tempos entre chegadas e tempos de serviço
    tec = gera_tempos(tec_distr,limite_simulacao)
    ts = gera_tempos(ts_distr,limite_simulacao)

    TR = TEC = TF = 0
    fila = []

    # data frame que guarda as informações da simulação
    colunas = ["Cliente","TEC","TR","Atendente","TS-I","TS","TS-F","TF"]
    simulacao = pd.DataFrame(columns=colunas)
    
    # quantidade de atendentes do sistema
    atendentes = [Atendente(i+1) for i in range(qtd_atendentes)]

    while chegadas < limite_simulacao:
        fila_cheia = False
        
        # Precisa gerar mais valores
        if len(tec) == 0:
            tec = gera_tempos(tec_distr,limite_simulacao)

        for atendente in atendentes:
            # atendente está desocupado
            if TR >= atendente.TS_F:
                atendente.TS_I = TR
                atendente_disponivel = atendente
                break
        
        # todos os atendentes estão ocupados
        else:
            # controlar quantidade de entidades presentes na fila
            for entidade in fila:
                tempo_inicio = entidade   # quando a entidade da fila vai ser atendida
                if TR >= tempo_inicio:
                    fila.remove(tempo_inicio) 

            tamanho_fila = len(fila)
            
            # não alcançou o limite da fila
            if tamanho_fila < limite_fila:
                # qual atendente ficará disponível primeiro
                atendente_disponivel = min(atendentes, key=lambda x: x.TS_F)
                atendente_disponivel.TS_I = atendente_disponivel.TS_F
                
                fila.append(atendente_disponivel.TS_I)
            
            else:
                fila_cheia = True
            
        # cliente pode ser atendido
        if not fila_cheia:
            atendente_disponivel.TS = ts.pop()
            atendente_disponivel.TS_F = atendente_disponivel.TS_I + atendente_disponivel.TS

            TF = atendente_disponivel.TS_I - TR

            simulacao.loc[chegadas] = [chegadas+1,TEC,TR,atendente_disponivel.nome,atendente_disponivel.TS_I, 
                atendente_disponivel.TS,atendente_disponivel.TS_F,TF]
            
            chegadas += 1
        
        # marca a próxima chegada
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
    tec_nome,tec_valor,ts_nome,ts_valor,limite_fila = menu()

    # distribuição do tec e ts
    tec_distr[tec_nome] = tec_valor
    ts_distr[ts_nome] = ts_valor
    
    resultado_simulacao = realiza_simulacao(atendentes,tec_distr,ts_distr,limite_fila)
    resultado_simulacao[["Cliente","Atendente"]] = resultado_simulacao[["Cliente","Atendente"]].astype(int)
    print(resultado_simulacao.to_string(index=False))

    # relatório das estatísticas
    print("\nNúmero Médio de Entidades nas Filas:", entidades_fila(resultado_simulacao))
    print("Tempo Médio de uma Entidade na Fila:", tempo_fila(resultado_simulacao))
    print("Tempo Médio no Sistema:", tempo_sistema(resultado_simulacao))

    medias = ocupacao_servidores(resultado_simulacao,atendentes)
    for atendente,media in enumerate(medias):
        print(f"Taxa Média de Ocupação do Servidor {atendente+1}:", media)
    
if __name__ == '__main__':
    main()
