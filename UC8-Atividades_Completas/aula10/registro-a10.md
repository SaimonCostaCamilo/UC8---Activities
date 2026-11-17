# Registro A10 — Interface gráfica de pedidos e validações

**Nome:** Saimon Camilo  
**Turma:** TDS  
**Data:** 13/11/2026

## Objetivo e conceitos
Consolidar a interface gráfica de pedidos, validação de entradas, atualização do carrinho e cálculo de pagamento mantendo as regras no modelo.

## Arquitetura
A lógica de pedido e pagamento permanece em módulos próprios; `main.py` cuida da janela e dos eventos; `verificar.py` executa os casos automatizados.

## Testes executados
`python -B verificar.py` — código de saída 0; previsões e resultados conferem.

**Situação:** suíte automatizada aprovada. O teste automatizado não substitui a observação visual e de teclado.
