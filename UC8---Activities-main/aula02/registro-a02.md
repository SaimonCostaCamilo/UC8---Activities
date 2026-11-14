# Registro A02 — Cadastro completo e controle de estado

**Nome:** Saimon Camilo  
**Turma:** TDS  
**Data:** 13/11/2026

## Objetivo e conceitos
Construir cadastro com estado, leitura de campos, validação, inclusão, listagem e limpeza. `get()` lê o conteúdo atual do campo; `int()` pode lançar `ValueError` se o texto não representar inteiro. Em `command`, passa-se a referência da função, sem executá-la durante a criação do botão.

## Retomada
- `get()` devolve o texto do widget; a conversão numérica precisa ser protegida por validação/tratamento de erro.
- Passar a função registra o callback; chamá-la imediatamente executa naquele momento.
- `strip()` permite detectar entrada vazia ou apenas espaços.

## Testes e evidências
Foram registrados os fluxos de exibir lista vazia, incluir cadastro fictício, exibir dados confirmados, limpar campos e recusar idade inválida depois de um cadastro válido. A observação registrada confirma inclusão, listagem e limpeza; a validação impede que entrada inválida seja adicionada.

**Situação:** testes manuais descritos no registro; sem suíte automatizada nesta aula.
