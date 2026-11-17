# Relatório da Aula 01 — Fundamentos de entrada, saída e cadastro

**Aluno:** Saimon Costa Camilo  
**Turma:** TDS  
**Data do relatório:** 12/11/2026

## 1. Objetivo da atividade

Praticar captura de dados, validação básica, processamento de entradas e apresentação de resultados no terminal e em uma interface Tkinter.

## 2. Arquivos e organização do projeto

- `terminal.py`: fluxo de entrada e saída pelo terminal.
- `cadastro.py`: cadastro com campos e validações.
- `evento.py`: exemplo de tratamento de evento.

## 3. Conceitos e decisões técnicas

- Separar o texto digitado do tipo de dado esperado.
- Validar nome e idade antes de apresentar a resposta.
- Tratar idade vazia, texto, zero, valor negativo e entrada decimal não inteira.

## 4. Execução e evidências

O registro A01 contém uma matriz preenchida com casos válidos e inválidos. Foram relatados resultados observados para nome composto, idade vazia, letras, zero e número negativo. A entrada decimal `2.5` foi identificada como caso que exigia validação específica. O registro também relata que os dados não persistem após fechar e reabrir, comportamento esperado para esta etapa.

## 5. Dificuldades, correções e pontos de atenção

O próprio registro aponta como dificuldade retomar o uso do Tkinter. A validação específica de números não inteiros e a conferência completa de teclado/interface devem ser revistas na execução local.

## 6. Conclusão

A atividade contribui para a evolução gradual do projeto da UC8. Este relatório foi elaborado a partir dos arquivos, README e registros existentes nesta pasta. Os testes são considerados concluídos somente quando há evidência explícita de execução; itens sem resultado observado permanecem identificados como pendentes, evitando registrar como realizado algo que não está comprovado.
