"""A03 — complete as funções antes de conectá-las à janela."""
def calcular(campos, registro):
    # TODO: ler reais e as duas cotações; aceitar vírgula ou ponto decimal.
    # TODO: tratar conversão inválida, reais negativos e cotações <= 0.
    # TODO: dividir reais por cada cotação.
    # TODO: confirmar entradas e os dois resultados somente após validar tudo.
    try:
        valor_real = float(campos["reais"].replace(',', '.'))
        valor_dolar = float(campos["cotacao_dolar"].replace(',', '.'))
        valor_euro = float(campos["cotacao_euro"].replace(',', '.'))
    except ValueError:
        return "Erro: Entrada inválida. Por favor, insira números válidos."
    
    if valor_real <= 0 or valor_dolar <= 0 or valor_euro <= 0:
        return "Erro: O valor em reais e as cotações devem ser maiores que zero."

    cotacao_real_dolar = valor_real / valor_dolar
    cotacao_real_euro = valor_real / valor_euro
    registro.append((valor_real, valor_dolar, valor_euro, cotacao_real_dolar, cotacao_real_euro))
    
    return f"Valores convertidos: {valor_real:.2f} reais = {cotacao_real_dolar:.2f} dólares, {cotacao_real_euro:.2f} euros."


def exibir(registro):
    # TODO: tratar ausência de conversão; consultar somente registro.
    #valores tratados no calcular
    # TODO: mostrar entradas usadas e resultados, estes com duas casas.
    print("exibindo registros")
    if not registro:
        return "Nenhuma conversão realizada ainda."
    return [tuple(round(valor,2)for valor in reg) for reg in registro]


def limpar(campos):
    # TODO: esvaziar os três campos; preservar registro e resultados.
    campos = {"reais": "", "cotacao_dolar": "", "cotacao_euro": ""}
    return f"Campos estão vazios agora: {campos}"


if __name__ == "__main__":
    campos = {"reais": "100", "cotacao_dolar": "5,5", "cotacao_euro": "4"}
    registro = []
    print(exibir(registro))
    print(calcular(campos, registro))
    print(exibir(registro))
    print(limpar(campos))
    print(exibir(registro))
    # Acrescente as outras sequências da matriz, prevendo antes de executar.
