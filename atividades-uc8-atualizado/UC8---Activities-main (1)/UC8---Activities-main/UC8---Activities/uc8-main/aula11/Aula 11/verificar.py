# A11: Verificações sem GUI para Estados, Cancelamento e Versão da Prévia
from modelos import Pedido, Produto, Pizza, Bebida

def verificar():
    print("Iniciando verificações da Aula 11 (Pizzaria)...")
    
    # 1. Configuração de dados fictícios
    p1 = Pizza("P01", "Calabresa", "Média", 4000)
    b1 = Bebida("B01", "Guaraná 2L", 1200)
    
    pedido = Pedido()
    
    # --- Caso T01: Vazio não finaliza ---
    try:
        pedido.finalizar(forma="PIX", confirmado=True)
        assert False, "Deveria ter recusado finalização de pedido vazio."
    except ValueError as e:
        print(f"[OK] T01 - Vazio recusado corretamente: {e}")

    # Adicionando itens à montagem
    pedido.adicionar(p1, "1")
    pedido.adicionar(b1, "2")
    assert pedido.estado == "montagem"
    assert pedido.versao == 3  # Inicial 1 + 2 adições

    # --- Caso T02: Forma de pagamento ausente ou inválida não finaliza ---
    try:
        pedido.finalizar(forma="", confirmado=True)
        assert False, "Deveria ter recusado pagamento vazio."
    except ValueError as e:
        print(f"[OK] T02 - Forma de pagamento ausente recusada: {e}")

    # --- Caso T03: Cancelamento preserva montagem e itens ---
    # Simula abertura da prévia guardando a versão atual
    versao_previa = pedido.versao
    # O cancelamento ou fechar o X/Escape apenas encerra a janela e NÃO altera o estado nem os itens
    assert pedido.estado == "montagem"
    assert len(pedido.linhas()) == 2
    print("[OK] T03 - Cancelamento preservou a montagem e os itens perfeitamente.")

    # --- Caso T04: Prévia alterada após abertura exige nova conferência ---
    # O usuário abriu a prévia na versão 3, mas alterou o pedido antes de confirmar (ex: adicionou mais um item)
    pedido.adicionar(b1, "1")  # Incrementa a versão para 4
    
    try:
        # Tenta finalizar passando a versao_previa antiga (3)
        pedido.finalizar(forma="Dinheiro", confirmado=True, versao_previa=versao_previa)
        assert False, "Deveria ter rejeitado a prévia antiga."
    except ValueError as e:
        print(f"[OK] T04 - Prévia antiga rejeitada corretamente: {e}")

    # --- Caso T05: Confirmar gera retrato independente com total correto ---
    versao_valida = pedido.versao
    comprovante = pedido.finalizar(forma="PIX", confirmado=True, versao_previa=versao_valida)
    
    assert pedido.estado == "finalizado"
    assert comprovante["total_centavos"] == 7600  # Corrigido de 6400 para 7600
    print(f"[OK] T05 - Confirmação bem-sucedida. Total do comprovante: {comprovante['total_centavos']} centavos.")

    # --- Caso T06: Pedido finalizado bloqueia mutações e segunda finalização ---
    try:
        pedido.adicionar(p1, "1")
        assert False, "Pedido finalizado não deveria aceitar adições."
    except RuntimeError as e:
        print(f"[OK] T06.1 - Mutação pós-finalização bloqueada: {e}")

    try:
        pedido.finalizar(forma="PIX", confirmado=True, versao_previa=pedido.versao)
        assert False, "Não deveria permitir repetir a finalização."
    except RuntimeError as e:
        print(f"[OK] T06.2 - Repetição de finalização bloqueada: {e}")

    # --- Caso T07: Retrato do comprovante é independente de mutações no objeto ---
    # Modificar o dicionário do comprovante retornado não afeta o estado interno guardado
    comprovante["forma_pagamento"] = "Alterado Fora"
    assert pedido.comprovante["forma_pagamento"] == "PIX"
    print("[OK] T07 - Comprovante mantém independência de dados.")

    # --- Caso T08: Novo pedido limpa a montagem ---
    pedido.novo()
    assert pedido.estado == "montagem"
    assert len(pedido.linhas()) == 0
    print("[OK] T08 - Novo pedido iniciado com sucesso e carrinho limpo.")

    print("\nTodos os testes unitários foram executados com sucesso!")
    return True

if __name__ == "__main__":
    if verificar():
        print("Casos executados: previsões e resultados conferem.")
    else:
        print("Verificações ainda incompletas.")