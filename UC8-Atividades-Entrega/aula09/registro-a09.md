# Registro A09 — Integração de interface, pedido e pagamento

**Nome:** Saimon Camilo  
**Turma:** TDS  
**Data:** 13/11/2026

## Objetivo e conceitos
Integrar seleção de itens, carrinho, atualização/remoção, pagamento e estado do pedido. A seleção deve ser validada antes de acessar a linha; o código do produto identifica o item independentemente da posição visual.

## Arquitetura
`modelos.py` mantém o pedido; `pagamento.py` calcula valores; `main.py` integra callbacks e interface; `verificar.py` executa a regressão.

## Testes executados
`python -B verificar.py` — código de saída 0; todas as verificações automatizadas passaram.

**Situação:** suíte automatizada aprovada. Conferência manual da janela permanece separada.
