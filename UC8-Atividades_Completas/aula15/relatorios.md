# Relatório da Aula 15 — CRUD de produtos e início do cadastro de clientes

**Aluno:** Saimon Costa Camilo  
**Turma:** TDS  
**Data do relatório:** 12/11/2026

## 1. Objetivo da atividade

Adicionar edição e exclusão de produtos por ID e iniciar o cadastro persistente de clientes, mantendo o contrato do repositório SQLite.

## 2. Arquivos e organização do projeto

- `main.py`: interface e callbacks.
- `repositorio.py`: CRUD e persistência.
- `modelos.py`, `pagamento.py`, `arquivos.py`, `relatorios.py` e `perfis.py`: módulos reaproveitados.
- `verificar.py`: testes automatizados.
- `ensaio.py`: apoio/ensaio da atividade.

## 3. Conceitos e decisões técnicas

- Editar pelo ID, não pela posição visual da linha.
- Distinguir inclusão (`INSERT`) de edição (`UPDATE`).
- Solicitar confirmação antes de excluir.
- Preservar registros e estado quando a exclusão é cancelada.
- Incluir e listar clientes com persistência SQLite.

## 4. Execução e evidências

O registro A15 relata aprovação dos testes automatizados T01–T04 e T06–T10, além da regressão A14. A edição por ID, reordenação da lista, rejeição de entrada inválida, ID inexistente, exclusão confirmada/cancelada, lista vazia e persistência de clientes são descritas. O teste de seleção na interface e o checklist visual permanecem pendentes de execução manual.

## 5. Dificuldades, correções e pontos de atenção

Executar `python verificar.py` e abrir `python main.py` em desktop para conferir Novo, editar, excluir, cancelar, lista vazia e cadastro de clientes.

## 6. Conclusão

A atividade contribui para a evolução gradual do projeto da UC8. Este relatório foi elaborado a partir dos arquivos, README e registros existentes nesta pasta. Os testes são considerados concluídos somente quando há evidência explícita de execução; itens sem resultado observado permanecem identificados como pendentes, evitando registrar como realizado algo que não está comprovado.
