# Registro A18 — Regressão, correções e README reproduzível

**Nome:** Saimon Camilo  
**Turma:** TDS  
**Data:** 13/11/2026

## Objetivo e arquitetura
Revisar a A17, corrigir validações sem alterar o estado válido, executar regressão e documentar reprodução em outra pasta. `modelos.py` contém pedido/quantidade; `pagamento.py` trata valores; `repositorio.py` mantém SQLite/transações; `controller.py` coordena operações; `main.py` apresenta a interface.

## Correções
- Quantidade aceita somente inteiro positivo (ou inteiro Python não booleano); floats, booleanos, zero, vazio e texto inválido são recusados.
- A validação ocorre antes da alteração, preservando quantidade e total anteriores em caso de erro.
- O parser monetário não descarta letras silenciosamente; entradas como `abc10` são rejeitadas.
- A interface oferece **Atualizar qtd.** para aplicar a nova quantidade validada.
- `SORVETERIA_DB` permite selecionar banco de ensaio separado.

## Testes executados
`python -B verificar.py` — código de saída 0; regressões A14–A17 e casos A18 T01–T06 passaram. `python -B ensaio-a18-logic.py` também concluiu com código 0. A cópia em outro diretório executou ambos os comandos com sucesso.

**Situação:** testes automatizados e reprodução em outra pasta aprovados. Testes visuais, Tab/Shift+Tab, foco, redimensionamento e validação por colega permanecem pendentes.
