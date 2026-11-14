# Registro A13 — Exportação de comprovantes, perfis e integração de módulos

**Nome:** Saimon Camilo  
**Turma:** TDS  
**Data:** 13/11/2026

## Objetivo e conceitos
Exportar CSV a partir de comprovante confirmado, preservar o relatório diante de cancelamento/falha e separar sessão de usuário do estado da venda.

## Testes executados
`python -B verificar.py` — código de saída 0. T00–T12 passaram, incluindo CSV com acentos/aspas/delimitadores, comprovante estável, cancelamento, falha de escrita, sessão, remoção do último item e regressões JSON/pagamento.

**Situação:** suíte de núcleo aprovada. `verificar_interface.py` não pôde ser concluído porque o ambiente de execução não possui display gráfico (`TclError: couldn't connect to display :0`); a inspeção visual permanece pendente.
