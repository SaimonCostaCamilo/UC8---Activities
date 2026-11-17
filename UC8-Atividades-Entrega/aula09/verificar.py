# Complete os casos do registro; não marque sucesso sem verificá-los.
from modelos import Produto, Item, Pedido, quantidade, formatar
from decimal import Decimal

def verificar():
    # TODO: criar dados fictícios, executar e comparar com assert.
    # TODO: testar erro após válido, limites e uma correção com nova execução.
    print("Iniciando verificações automatizadas (A09)...")

    prod1 = Produto("P01", "Sorvete Chocolate", 500)
    prod2 = Produto("P02", "Sorvete Morango", 450) 
    prod3 = Produto("P03", "Açaí Tradicional", 1000)

    pedido = Pedido()

    pedido.adicionar(prod1, "2")
    pedido.adicionar(prod2, "1")

    assert pedido.total_centavos() == 1450, f"Esperado 1450 centavos, obtido {pedido.total_centavos()}"

    linhas_iniciais = pedido.linhas()
    ids_visuais = [linha[0] for linha in linhas_iniciais]
    assert ids_visuais == ["P01", "P02"], f"Ordem inicial incorreta: {ids_visuais}"

    ids_visuais.reverse()
    assert ids_visuais == ["P02", "P01"], "A reordenação visual falhou."
    assert pedido._itens["P01"].produto.nome == "Sorvete Chocolate", "A identidade do produto foi perdida após reordenação."

    pedido.atualizar("P01", "4")
    assert pedido._itens["P01"].quantidade == 4, "A quantidade do item P01 não foi atualizada corretamente."
    assert pedido.total_centavos() == 2450, f"Total incorreto após atualização: {pedido.total_centavos()}"

    pedido.remover("P02")
    assert "P02" not in pedido._itens, "O produto P02 deveria ter sido removido."
    assert pedido.total_centavos() == 2000, "O total deveria ser apenas o do P01 (2000 centavos)."

    pedido.remover("P01")
    assert len(pedido._itens) == 0, "O carrinho deveria estar completamente vazio."
    assert pedido.total_centavos() == 0, "O total do carrinho vazio deve ser zero."

    try:
        pedido.atualizar("XPTO", "2")
        assert False, "Deveria ter lançado KeyError para código inexistente na atualização."
    except KeyError:
        pass

    try:
        pedido.remover("XPTO")
        assert False, "Deveria ter lançado KeyError para código inexistente na remoção."
    except KeyError:
        pass

    try:
        quantidade("-5")
        assert False, "Deveria recusar quantidade negativa."
    except ValueError:
        pass

    print("Todas as verificações automatizadas passaram com sucesso!")
    return True

if __name__ == "__main__":
    if verificar():
        print("Casos executados: previsões e resultados conferem.")
    else:
        print("Verificações ainda incompletas.")
