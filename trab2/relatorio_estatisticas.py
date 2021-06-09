# Taxa Média de Ocupação dos Servidores
def ocupacao_servidores(simulacao, qtd_atendentes):
    for nome_atendente in range(1,qtd_atendentes+1):
        atendente = simulacao.loc[simulacao["Atendente"] == nome_atendente]
        atendente = atendente.reset_index(drop=True)

        soma_tempo_servico = atendente["TS"].sum()
        periodo = (atendente.iloc[-1:]["TS-F"]).item()   # último tempo de serviço do atendente 
        
        ocupacao_servidor = soma_tempo_servico/periodo
        print(f"Taxa Média de Ocupação do Servidor {nome_atendente}:", ocupacao_servidor)


# Tempo Médio de uma Entidade na Fila
def tempo_entidade_fila(simulacao):
    entidades = simulacao.loc[simulacao["TF"] > 0]   # entidades que entraram na fila
    soma_tempos = entidades["TF"].sum()   # soma dos tempos que as entidades ficaram na fila
    qtd_entidades = entidades.shape[0]   # quantas entidades entraram na fila
    
    if qtd_entidades > 0:
        media = soma_tempos/qtd_entidades
    else:
        media = 0
    
    print("Tempo Médio de uma Entidade na Fila:", media)

# Tempo Médio no Sistema
def tempo_sistema():
    pass
