# Registro A11 — Pizzaria: estados do pedido, prévia e confirmação

**Nome:** Saimon Camilo  
**Turma:** TDS  
**Data:** 13/11/2026

## Objetivo e conceitos
Controlar montagem, prévia, cancelamento e confirmação de pedido. Uma prévia antiga não pode confirmar uma montagem alterada; a finalização deve ocorrer uma única vez e gerar comprovante independente.

## Testes executados
Na pasta `Aula 11`: `python -B verificar.py` — código de saída 0. T01–T08 passaram: pedido vazio, pagamento obrigatório, cancelamento, prévia desatualizada, confirmação, mutação/repetição após finalização, independência do comprovante e início de novo pedido.

**Situação:** suíte automatizada aprovada.
