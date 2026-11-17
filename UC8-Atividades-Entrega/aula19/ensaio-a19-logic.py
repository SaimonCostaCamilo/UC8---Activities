"""Roteiro curto: problema, fluxo válido, recusa e correção."""
roteiro = [
    ("Problema", "registrar uma venda fictícia sem perder o histórico"),
    ("Válido", "consultar duas vendas fictícias por seus IDs"),
    ("Recusa", "tentar criar backup em destino já existente"),
    ("Correção", "informar um caminho novo e conferir a cópia"),
]
for etapa, acao in roteiro:
    print(f"{etapa} -> {acao}")
