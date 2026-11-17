# Registro A14 — Persistência SQLite e validações do repositório

**Nome:** Saimon Camilo  
**Turma:** TDS  
**Data:** 13/11/2026

## Objetivo e conceitos
Persistir produtos e clientes em SQLite, usar IDs como identidade, parametrizar SQL e manter pedido em memória. O banco é reaberto pelo mesmo caminho sem apagar registros existentes.

## Testes executados
`python -B verificar.py` — código de saída 0. T00–T13 passaram: importação sem criação prematura, tabelas idempotentes, centavos, apóstrofo, validações, IDs, reabertura, falha de conexão, pagamento, pedido, sessão, JSON, CSV e clientes.

**Situação:** suíte automatizada aprovada; interface não foi validada visualmente.
