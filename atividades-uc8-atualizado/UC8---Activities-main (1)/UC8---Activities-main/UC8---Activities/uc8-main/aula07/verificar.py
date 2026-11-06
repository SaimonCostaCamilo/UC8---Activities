# Complete os casos do registro; não marque sucesso sem verificá-los.
from modelos import Produto, Pedido, quantidade, formatar


def verificar():
    # TODO: criar dados fictícios, executar e comparar com assert.
    fruta = Produto("F01", "Fruta", 150)
    leite = Produto("L01", "Leite", 300)

    pedido = Pedido()
    pedido.adicionar(fruta, "2")
    pedido.adicionar(leite, "3")

    assert len(pedido.itens) == 2
    assert pedido.itens[0].quantidade == 2
    assert pedido.itens[1].quantidade == 3
    assert pedido.itens[0].subtotal() == 300
    assert pedido.itens[1].subtotal() == 900
    assert pedido.total_centavos() == 1200
    assert formatar(1200) == "R$ 12,00"

    # TODO: testar erro após válido — repetição por código preserva pedido.
    itens_antes = len(pedido.itens)
    try:
        pedido.adicionar(fruta, "1")
        assert False, "deveria ter levantado ValueError"
    except ValueError as e:
        assert "ja esta no pedido" in str(e)
    assert len(pedido.itens) == itens_antes

    # quantidade invalida preserva pedido
    outro = Produto("A01", "Outro", 200)
    try:
        pedido.adicionar(outro, "0")
        assert False, "deveria ter levantado ValueError"
    except ValueError:
        pass
    assert len(pedido.itens) == itens_antes

    try:
        pedido.adicionar(outro, "abc")
        assert False, "deveria ter levantado ValueError"
    except ValueError:
        pass
    assert len(pedido.itens) == itens_antes

    # TODO: testar limites — quantidade 1 e valor alto.
    p2 = Produto("B01", "Produto B", 9999)
    pedido2 = Pedido()
    pedido2.adicionar(p2, "1")
    assert pedido2.itens[0].quantidade == 1
    assert pedido2.itens[0].subtotal() == 9999
    assert formatar(9999) == "R$ 99,99"

    # pedido fechado recusa adicionar
    pedido2.aberto = False
    try:
        pedido2.adicionar(fruta, "1")
        assert False, "deveria ter levantado RuntimeError"
    except RuntimeError as e:
        assert "fechado" in str(e)

    # linhas inclui total
    linhas = pedido.linhas()
    assert any("Total" in l for l in linhas)
    assert any("F01" in l for l in linhas)
    assert any("L01" in l for l in linhas)

    # uma correcao: nova execucao com quantidade corrigida
    pedido3 = Pedido()
    pedido3.adicionar(fruta, "5")
    assert pedido3.total_centavos() == 750
    assert formatar(750) == "R$ 7,50"

    return True


if __name__ == "__main__":
    if verificar():
        print("Casos executados: previsoes e resultados conferem.")
    else:
        print("Verificacoes ainda incompletas.")
