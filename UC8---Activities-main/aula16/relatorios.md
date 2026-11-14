# Relatório da Aula 16 — Controller, repositórios e CRUD completo de clientes

**Aluno:** Saimon Costa Camilo  
**Turma:** TDS  
**Data do relatório:** 12/11/2026

## 1. Objetivo da atividade

Separar a coordenação das operações de cadastro da interface e permitir que a mesma lógica trabalhe com armazenamento SQLite ou em memória.

## 2. Arquivos e organização do projeto

- `controller.py`: coordenação de listar, salvar e excluir.
- `memoria.py`: repositório em memória com contrato equivalente.
- `repositorio.py`: implementação SQLite.
- `main.py`: interface Tkinter.
- `modelos.py`, `pagamento.py`, `arquivos.py`, `relatorios.py` e `perfis.py`: módulos integrados.
- `verificar.py`: testes automatizados.

## 3. Conceitos e decisões técnicas

- Manter controller independente de Tkinter.
- Usar argumentos, formatos de retorno e erros compatíveis entre repositórios.
- Criar e editar produtos/clientes por ID.
- Retornar cópias defensivas na implementação em memória.
- Preservar campos após cancelamento ou falha.
- Manter pedido em memória e produtos/clientes persistidos.

## 4. Execução e evidências

O registro A16 informa que `python -B verificar.py` terminou com código 0 e que os casos automatizados A14, A15 e A16 foram aprovados. Inclui testes de contrato comum, CRUD por ID, cancelamento, exclusão confirmada, validação, cópia defensiva e persistência SQLite. A janela Tkinter real está marcada como pendente de conferência manual.

## 5. Dificuldades, correções e pontos de atenção

Executar `python main.py` em ambiente gráfico para conferir os callbacks, o cancelamento via diálogo e a preservação dos campos após falha de gravação.

## 6. Conclusão

A atividade contribui para a evolução gradual do projeto da UC8. Este relatório foi elaborado a partir dos arquivos, README e registros existentes nesta pasta. Os testes são considerados concluídos somente quando há evidência explícita de execução; itens sem resultado observado permanecem identificados como pendentes, evitando registrar como realizado algo que não está comprovado.
