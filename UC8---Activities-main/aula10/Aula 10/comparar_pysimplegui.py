# A10: Demonstração de uso dos modelos de pedido, pizza e bebida.
from modelos import Pizza, Bebida, Pedido

def demonstrar():
    """
    Demonstra a criação de um pedido com uma pizza média de mussarela (3500 centavos)
    e duas bebidas (600 centavos cada), validando o total esperado de 4700 centavos
    sem depender de interface gráfica.
    """
    print("Iniciando demonstração do modelo da pizzaria (A10)...")
    
    # 1. Criação do pedido e dos produtos
    pedido = Pedido()
    pizza_mussarela = Pizza(codigo="P01", nome="Mussarela", tamanho="Média", preco_centavos=3500)
    bebida_refri = Bebida(codigo="B01", nome="Refrigerante", preco_centavos=600)
    
    # 2. Adicionando itens ao pedido
    pedido.adicionar(pizza_mussarela, "1")  # 1x 3500
    pedido.adicionar(bebida_refri, "2")     # 2x 600
    
    # 3. Conferindo linhas e total
    print("\nItens no Pedido:")
    for linha in pedido.linhas():
        print(f" - {linha['quantidade']}x {linha['nome']} | Subtotal: R$ {linha['subtotal'] / 100:.2f}")
    
    total = pedido.total_centavos()
    print(f"\nTotal calculado: {total} centavos (Esperado: 4700 centavos)")
    
    assert total == 4700, f"Erro na demonstração: esperado 4700, obtido {total}"
    print("Demonstração concluída com sucesso e validada por assert!")
    return True

if __name__ == "__main__":
    demonstrar()