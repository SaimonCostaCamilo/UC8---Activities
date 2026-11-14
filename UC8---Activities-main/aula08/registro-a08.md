# Registro A08 — Carrinho, pagamento e arredondamento decimal

**Nome:** Saimon Camilo  
**Turma:** TDS  
**Data:** 13/11/2026

## Objetivo e conceitos
Separar modelo de pedido e cálculo de pagamento, usar valores decimais/centavos para evitar erros de ponto flutuante e validar estados do carrinho.

## Arquitetura
`modelos.py` representa produtos, itens e pedido; `pagamento.py` calcula valores; `main.py` conecta a interface; `verificar.py` executa testes sem depender da janela.

## Testes executados
`python -B verificar.py` — código de saída 0; a suíte informou que previsões e resultados conferem.

**Situação:** suíte automatizada aprovada. A execução não equivale à inspeção visual da interface.
