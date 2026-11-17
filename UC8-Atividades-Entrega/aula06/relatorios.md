# Relatório da Aula 06 — Modelagem de aluno e validação de dados

**Aluno:** Saimon Costa Camilo  
**Turma:** TDS  
**Data do relatório:** 12/11/2026

## 1. Objetivo da atividade

Introduzir classes e objetos para representar alunos, manter dados independentes por instância e validar a confirmação integral de um conjunto de notas.

## 2. Arquivos e organização do projeto

- `aluno.py`: classe e regras do objeto Aluno.
- `verificar_modelo.py`: verificações automatizadas do modelo.

## 3. Conceitos e decisões técnicas

- Distinguir classe, instância, `__init__` e `self`.
- Manter coleções próprias em cada objeto, evitando compartilhamento acidental.
- Validar identificação e exatamente cinco notas antes de atualizar o objeto.
- Preservar todos os atributos do último estado válido quando uma tentativa falha.

## 4. Execução e evidências

O registro A06 lista 17 testes planejados, cobrindo importação sem interface, independência de objetos, cálculo de médias, validação, cópia de listas e consultas. Os campos de previsão, observado e correção/reteste estão vazios no registro disponível; assim, não há evidência documental suficiente para marcar esses testes como concluídos.

## 5. Dificuldades, correções e pontos de atenção

Executar `python verificar_modelo.py`, preencher os resultados efetivamente observados e completar a demonstração de dois objetos independentes. A interface e os testes de consulta também precisam de conferência local.

## 6. Conclusão

A atividade contribui para a evolução gradual do projeto da UC8. Este relatório foi elaborado a partir dos arquivos, README e registros existentes nesta pasta. Os testes são considerados concluídos somente quando há evidência explícita de execução; itens sem resultado observado permanecem identificados como pendentes, evitando registrar como realizado algo que não está comprovado.
