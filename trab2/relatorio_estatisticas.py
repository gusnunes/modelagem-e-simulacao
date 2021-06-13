# Número Médio de Entidades nas Filas
def entidades_fila(simulacao):
    # tempo final da simulação
    tempo_final = simulacao["TS-F"].max()

    # soma dos tempos que as entidades ficaram na fila 
    soma_tempos = simulacao["TF"].sum()

    numero_medio = soma_tempos/tempo_final
    print("Número Médio de Entidades nas Filas:", numero_medio)

# Taxa Média de Ocupação dos Servidores
def ocupacao_servidores(simulacao, qtd_atendentes):
    for nome_atendente in range(1,qtd_atendentes+1):
        atendente = simulacao.loc[simulacao["Atendente"] == nome_atendente]
        atendente = atendente.reset_index(drop=True)

        # servidor atendeu pelo menos um cliente
        if not atendente.empty:
            soma_tempo_servico = atendente["TS"].sum()
            periodo = (atendente.iloc[-1:]["TS-F"]).item()   # último tempo de serviço do atendente 
            
            ocupacao_servidor = soma_tempo_servico/periodo
            print(f"Taxa Média de Ocupação do Servidor {nome_atendente}:", ocupacao_servidor)


# Tempo Médio de uma Entidade na Fila
def tempo_fila(simulacao):
    entidades = simulacao.loc[simulacao["TF"] > 0]   # entidades que entraram na fila
    soma_tempos = entidades["TF"].sum()   # soma dos tempos que as entidades ficaram na fila
    qtd_entidades = entidades.shape[0]   # quantas entidades entraram na fila
    
    if qtd_entidades > 0:
        media = soma_tempos/qtd_entidades
    else:
        media = 0
    
    print("Tempo Médio de uma Entidade na Fila:", media)

# Tempo Médio no Sistema
def tempo_sistema(simulacao):
    tempo_sistema = 0
    qtd_clientes = simulacao.shape[0]

    for cliente in simulacao.itertuples(index=False):
        # entrada e saida do cliente do sistema
        tempo_entrada = cliente[simulacao.columns.get_loc("TR")] 
        tempo_saida = cliente[simulacao.columns.get_loc("TS-F")]

        # tempo que o cliente permaneceu no sistema
        tempo_cliente = tempo_saida - tempo_entrada

        # a soma dos tempos de todos os clientes
        tempo_sistema += tempo_cliente
        
    print("Tempo Médio no Sistema:", tempo_sistema/qtd_clientes)