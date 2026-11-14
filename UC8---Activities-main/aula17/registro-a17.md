# Registro A17 — Sorveteria integrada, transação de venda/itens, revisão de catálogo e CSV

**Nome:** Saimon Camilo  
**Turma:** TDS  
**Data:** 13/11/2026

## Objetivo e conceitos
Integrar catálogo, clientes, pedido, pagamento, transação SQLite, histórico e exportação CSV. A venda e seus itens devem ser gravados atomicamente; só após sucesso o pedido é finalizado.

## Testes executados
`python -B verificar.py` — código de saída 0. Regressões A14–A16 e casos A17 passaram: reabertura de catálogo/clientes/vendas, catálogo desatualizado, cliente inválido, pagamento PIX, rollback provocado, finalização única, bloqueio de exclusão vinculada e CSV.

**Situação:** suíte automatizada aprovada. Comparação visual ttk/CTk e testes de teclado/redimensionamento não foram executados.
