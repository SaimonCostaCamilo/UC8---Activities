# A10: Verificações sem GUI para Pizzaria (modelos, itens e pedido)
from modelos import Produto, Pizza, Bebida, Item, Pedido, quantidade, formatar

def verificar():
    try:
        # 1. Criação de dados fictícios e produtos
        pizza_mussarela = Pizza(codigo="P01", nome="Mussarela", tamanho="Média", preco_centavos=3500)
        bebida_refri = Bebida(codigo="B01", nome="Refrigerante", preco_centavos=600)
        
        pedido = Pedido()
        
        # 2. Executar adição do caso principal: Mussarela média (3500) + 2x Bebidas (600 cada = 1200) -> Total: 4700
        pedido.adicionar(pizza_mussarela, "1")
        pedido.adicionar(bebida_refri, "2")
        
        total_obtido = pedido.total_centavos()
        total_esperado = 4700
        
        assert total_obtido == total_esperado, f"Erro no total: esperado {total_esperado}, obtido {total_obtido}"
        
        # Conferir linhas geradas
        linhas = pedido.linhas()
        assert len(linhas) == 2, f"Esperado 2 linhas no pedido, encontrado {len(linhas)}"
        
        # 3. Testar erro após válido (tamanho de pizza inválido)
        pizza_invalida_criada = True
        try:
            Pizza(codigo="P99", nome="Calabresa", tamanho="Gigante", preco_centavos=4000)
            pizza_invalida_criada = False
        except ValueError:
            pass  # Exceção esperada para tamanho inválido
            
        assert pizza_invalida_criada, "Deveria ter recusado tamanho de pizza inválido ('Gigante')."
        
        # 4. Testar limites e recusa de quantidade inválida (mantendo o pedido anterior intacto)
        quantidade_recusada = False
        try:
            pedido.adicionar(bebida_refri, "abc")
        except ValueError:
            quantidade_recusada = True
            
        assert quantidade_recusada, "Deveria ter recusado quantidade com texto não numérico."
        
        # Conferir que o estado anterior do pedido permaneceu inalterado após a falha
        assert pedido.total_centavos() == 4700, "O total do pedido mudou após uma exceção de entrada."
        
        # 5. Correção e nova execução: atualizar quantidade de um item existente de forma válida
        pedido.atualizar("B01", "3") # Mudando de 2 para 3 bebidas (3 * 600 = 1800 + 3500 = 5300)
        assert pedido.total_centavos() == 5300, f"Erro após atualização: esperado 5300, obtido {pedido.total_centavos()}"
        
        return True

    except AssertionError as e:
        print(f"Falha na verificação (AssertionError): {e}")
        return False
    except Exception as e:
        print(f"Erro inesperado durante as verificações: {e}")
        return False


if __name__ == "__main__":
    if verificar():
        print("Casos executados: previsões e resultados conferem.")
    else:
        print("Verificações ainda incompletas.")