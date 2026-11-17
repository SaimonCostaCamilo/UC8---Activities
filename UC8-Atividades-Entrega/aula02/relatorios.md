# Relatório da Aula 02 — Cadastro completo e controle de estado

**Aluno:** Saimon Costa Camilo  
**Turma:** TDS  
**Data do relatório:** 12/11/2026

## 1. Objetivo da atividade

Construir um cadastro com múltiplos campos, manter registros confirmados separados dos campos editáveis e controlar as ações da interface.

## 2. Arquivos e organização do projeto

- `cadastro_completo.py`: interface e fluxo de cadastro.
- `estado_cadastro.py`: organização do estado dos registros.

## 3. Conceitos e decisões técnicas

- Usar `get()` para obter o conteúdo dos campos e converter tipos com validação.
- Associar callbacks aos botões sem executar a função durante a montagem da interface.
- Usar `strip()` para identificar entradas vazias ou compostas apenas por espaços.
- Manter os registros em uma estrutura independente dos campos visuais.

## 4. Execução e evidências

O registro A02 documenta testes de exibição antes do primeiro cadastro, inclusão, edição dos campos sem confirmação, limpeza, entradas inválidas e reabertura do programa. O aluno relata comportamento esperado para os casos de inclusão e validação, e observa que limpar os campos não deve apagar os registros já confirmados.

## 5. Dificuldades, correções e pontos de atenção

O registro menciona que a navegação por Tab/Shift+Tab percorre os controles, mas que o acionamento por teclado ainda precisava de ajuste. A apresentação da lista em aviso também foi apontada como melhoria possível.

## 6. Conclusão

A atividade contribui para a evolução gradual do projeto da UC8. Este relatório foi elaborado a partir dos arquivos, README e registros existentes nesta pasta. Os testes são considerados concluídos somente quando há evidência explícita de execução; itens sem resultado observado permanecem identificados como pendentes, evitando registrar como realizado algo que não está comprovado.
