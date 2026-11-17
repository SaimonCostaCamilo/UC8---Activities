# Meu registro A19 — Academia e demonstrações individuais

**Nome:** Saimon Camilo  
**Turma:** TDS  
**Data:** 13/11/2026

## Arquitetura e responsabilidades
- `main.py`: inicia a janela Tkinter da academia.
- `academia_ui.py`: abas Alunos, Planos, Matrículas e Backup SQLite; recebe ações e apresenta resultados.
- `repositorio_academia.py`: valida campos básicos e persiste alunos, planos e matrículas em SQLite.
- `backup_sqlite.py`: copia banco existente para destino novo por `Connection.backup()` e verifica integridade.
- `verificar.py`: testa backup e repositório em diretórios temporários.
- `referencia-a18/`: candidata desktop da sorveteria A18, preservada para retomada do projeto integrador.

## Matriz técnica de execução

| Caso | Evidência automatizada | Resultado |
|---|---|---|
| Backup em destino novo | `python -B verificar.py` — cópia aberta por outra conexão, `integrity_check=ok`, consulta de dois registros conhecidos | Aprovado |
| Origem preservada | Consulta após backup retorna os registros originais | Aprovado |
| Destino existente | Reexecução recusada; bytes da cópia anterior permanecem iguais | Aprovado |
| Origem ausente | `FileNotFoundError`; destino não é criado | Aprovado |
| Caminhos iguais | Operação recusada; banco original permanece íntegro | Aprovado |
| Persistência da janela | Cadastro de aluno/plano/matrícula e leitura de volta no repositório SQLite temporário | Aprovado |
| Exclusão vinculada | Repositório recusa excluir aluno/plano que possua matrícula | Aprovado |

Comando executado nesta revisão: `python -B verificar.py` na pasta `aula19`; todos os asserts passaram.

## Demonstração individual
Roteiro: abrir `main.py`, cadastrar aluno e plano fictícios, anotar IDs, criar matrícula, consultar listagem e realizar backup para destino novo. O roteiro de fala está em `roteiro-demo.md`.

**Preencher após executar pessoalmente:**
- Data/ambiente e versão Python:
- Fluxo válido observado na janela:
- Erro/cancelamento e mensagem observada:
- Backup manual criado e caminho escolhido:
- Pergunta técnica recebida e explicação dada:
- Feedback real de colega/professor (pessoa/contexto e comentário literal):

## Checklist da interface — inspeção presencial
- [ ] Conferir rótulos, controles e tabelas.
- [ ] Percorrer campos e botões com Tab e Shift+Tab.
- [ ] Conferir foco visível e acionamento por Enter.
- [ ] Provocar campo inválido, ler a mensagem e corrigir.
- [ ] Redimensionar a janela e verificar se tabelas/controles permanecem acessíveis.

Esses itens não são declarados como concluídos por testes sem interação visual. Marque somente após observar no desktop.

## Relação com a A20
A A20 amplia a demonstração de academia com validação de vínculos por ID e integridade referencial real no SQLite. A candidata A18 permanece preservada para a revalidação do projeto integrador, conforme `aula20/roteiro-revalidacao-a19.md`.
