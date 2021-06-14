def menu():
    # Opções dos Tempos entre Chegadas
    tec_option = input("O TEC é deterministico? [s/n]: ")
    if tec_option == 's':
        tec_valor = float(input("Digite o TEC: "))
        tec_nome = "deterministico"

    else:
        tec_option = input("Distribuição do TEC? [exponencial/normal]: ")
        if tec_option == "exponencial":
            tec_nome = "exponencial"
            tec_valor = float(input("Digite a média: "))
        else:
            tec_nome = "normal"
            parametros = input("Digite a média e desvio padrão: ").split()
            tec_valor = (float(parametros[0]),float(parametros[1]))

    # Opções dos Tempo de Serviços
    ts_option = input("O TS é deterministico? [s/n]: ")
    if ts_option == 's':
        ts_valor = float(input("Digite o TS: "))
        ts_nome = "deterministico"

    else:
        ts_option = input("Distribuição do TS? [exponencial/normal]: ")
        if ts_option == "exponencial":
            ts_nome = "exponencial"
            ts_valor = float(input("Digite a média: "))
        else:
            ts_nome = "normal"
            parametros = input("Digite a média e desvio padrão: ").split()
            ts_valor = (float(parametros[0]),float(parametros[1]))
    
    # Opções de limite de fila
    fila_opcao = input("Limite de fila? [s/n]: ")
    if fila_opcao == 's':
        limite_fila = int(input("Digite o limite da fila: "))
    else:
        limite_fila = float("inf")

    return (tec_nome,tec_valor,ts_nome,ts_valor,limite_fila)