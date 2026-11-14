# Complete os casos do registro; não marque sucesso sem verificá-los.
from decimal import Decimal
from modelos import Produto, Pedido
from pagamento import calcular_pagamento, preco_para_centavos

def verificar():
    # TODO: criar dados fictícios, executar e comparar com assert.
    # TODO: testar erro após válido, limites e uma correção com nova execução.
    subtotal_base = "100.00"

    res_dinheiro = calcular_pagamento(subtotal_base, "Dinheiro")
    assert res_dinheiro["total"] == Decimal("87.00"), f"Esperado 87.00, obtido {res_dinheiro['total']}"
    assert res_dinheiro["desconto"] == Decimal("13.00")

    res_pix = calcular_pagamento(subtotal_base, "PIX")
    assert res_pix["total"] == Decimal("87.00")

    res_debito = calcular_pagamento(subtotal_base, "Débito")
    assert res_debito["total"] == Decimal("92.00")
    assert res_debito["desconto"] == Decimal("8.00")

    res_credito = calcular_pagamento(subtotal_base, "Crédito 1x")
    assert res_credito["total"] == Decimal("100.00")
    assert res_credito["desconto"] == Decimal("0.00")

    res_fracionario = calcular_pagamento("0.50", "PIX")
    assert res_fracionario["total"] == Decimal("0.44"), f"Esperado 0.44, obtido {res_fracionario['total']}"

    primeira_chamada = calcular_pagamento("100.00", "PIX")
    segunda_chamada = calcular_pagamento("100.00", "PIX")
    assert primeira_chamada["total"] == segunda_chamada["total"], "A repetição da chamada não pode alterar o resultado."
    assert segunda_chamada["total"] == Decimal("87.00")

    p = Produto("P01", "Sorvete", 10000)
    pedido = Pedido()
    pedido.adicionar(p, "1")

    subtotal_pedido_str = str(Decimal(pedido.total_centavos()) / 100)
    res_pedido = calcular_pagamento(subtotal_pedido_str, "Dinheiro")

    assert len(pedido.linhas()) == 1
    assert pedido.total_centavos() == 10000
    assert res_pedido["total"] == Decimal("87.00")

    return True

if __name__ == "__main__":
    if verificar():
        print("Casos executados: previsões e resultados conferem.")
    else:
        print("Verificações ainda incompletas.")
