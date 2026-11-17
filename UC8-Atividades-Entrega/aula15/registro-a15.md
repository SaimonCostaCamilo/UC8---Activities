# Registro A15 — CRUD de produtos por ID e início do cadastro de clientes

**Nome:** Saimon Camilo  
**Turma:** TDS  
**Data:** 13/11/2026

## Objetivo e conceitos
Implementar inclusão, edição e exclusão de produtos por ID e iniciar o cadastro persistente de clientes. A edição usa `UPDATE` no ID selecionado; não deve inserir duplicata nem depender da posição visual.

## Testes executados
`python -B verificar.py` — código de saída 0. Regressão A14 e casos A15 T14–T16 passaram: edição pelo mesmo ID após reordenação, preservação em entrada inválida, ID inexistente, cancelamento, exclusão confirmada, lista vazia e persistência de clientes.

**Situação:** suíte automatizada aprovada. A interação visual da janela não foi testada nesta execução.
