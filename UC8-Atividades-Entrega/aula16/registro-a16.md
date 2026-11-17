# Registro A16 — Controller, contratos de repositório, CRUD completo de clientes e persistência SQLite

**Nome:** Saimon Camilo  
**Turma:** TDS  
**Data:** 13/11/2026

## Objetivo e conceitos
Separar interface, controller e persistência. O controller usa um contrato comum para repositório em memória e SQLite; operações de edição/exclusão usam ID explícito.

## Testes executados
`python -B verificar.py` — código de saída 0. Regressões A14/A15 e A16 T17 passaram: contrato comum, CRUD por ID, cancelamento, validação, cópia defensiva e persistência.

**Situação:** suíte automatizada aprovada. A janela Tkinter não foi aberta; testes visuais e de teclado permanecem pendentes.
