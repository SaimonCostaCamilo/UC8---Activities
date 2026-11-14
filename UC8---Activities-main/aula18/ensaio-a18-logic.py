"""Ensaio independente de regressão da montagem do pedido (A18)."""
from modelos import Pedido, Produto

pedido = Pedido()
produto = Produto("E1", "Sorvete de teste", 650)

# Previsão calculada antes da chamada: 2 x 650 centavos = 1.300 centavos.
esperado = 1300
pedido.adicionar(produto, "2")
assert pedido.total_centavos() == esperado

# Entrada inválida deve falhar sem perder o pedido válido.
antes = pedido.linhas()
try:
    pedido.atualizar("E1", "0")
except ValueError:
    pass
else:
    raise AssertionError("Quantidade zero deveria ser recusada.")
assert pedido.linhas() == antes

# Reteste corrigido e caso vizinho.
pedido.atualizar("E1", "1")
assert pedido.total_centavos() == 650
pedido.remover("E1")
assert pedido.total_centavos() == 0
print("A18: erro preserva montagem; correção, remoção e pedido vazio conferidos.")

# Demonstração didática: previsão falsa é detectada, sem ocultar falha na suíte real.
try:
    assert pedido.total_centavos() == 99
except AssertionError:
    print("A18: previsão falsa detectada.")
else:
    raise AssertionError("O assert propositalmente falso deveria falhar.")
