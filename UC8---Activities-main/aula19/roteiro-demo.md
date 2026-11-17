# Minha demonstração individual — A19

## Versão apresentada
- Projeto: Sorveteria desktop (candidata A18).
- Origem da candidata: `referencia-a18/`, copiada do pacote `UC8---Activities-main (2).zip`.
- README testado: `referencia-a18/README-A18.md`.
- Alterações feitas depois da A18: nenhum arquivo da candidata A18 foi alterado nesta A19; os scripts de backup e ensaio estão separados nesta pasta.
- Caso reproduzível: regressão A14–A18 e ensaio de quantidade inválida/correção, conforme os comandos abaixo.

## Demonstração — problema, ação, resultado e limite
1. Problema/requisito: garantir que a montagem de uma venda continue íntegra após uma entrada inválida.
2. Comando: `python -B verificar.py` dentro de `referencia-a18/`.
3. Resultado observado nesta execução: suíte A14–A18 terminou com código 0; T01 da A18 confirmou que quantidade inválida preserva a montagem, quantidade 1 atualiza e remoção deixa pedido vazio.
4. Recusa/correção: `python -B ensaio-a18-logic.py` reproduziu erro com quantidade inválida, correção e remoção; saída terminou com código 0.
5. Persistência/relatório: a suíte testa persistência SQLite, reabertura e CSV com dados temporários; o ensaio A19 abaixo confere a cópia por outra conexão.
6. Limite: a execução automatizada não substitui inspeção visual da GUI, foco/Tab/Shift+Tab, redimensionamento ou demonstração presencial por colega.

## Decisão técnica explicada
A montagem do pedido fica em memória até a confirmação; a venda e seus itens são gravados na mesma transação SQLite. Isso evita persistir uma venda incompleta. A evidência está em `referencia-a18/modelos.py`, `referencia-a18/repositorio.py` e nos testes de rollback/reabertura de `referencia-a18/verificar.py`. O backup A19 usa `Connection.backup()` e não copia o arquivo enquanto está aberto.

## Comparação com a amostra de academia
- Entidades/IDs: `ALUNOS` (41, 92), `PLANOS` (7) e `MATRICULAS` (101), com vínculos `aluno_id` e `plano_id`.
- Responsabilidades: `models` representa entidades; `utils/persistencia.py` representa JSON; `controllers` coordena consulta; `views` seria a interface, não implementada na amostra.
- Limite da leitura: a amostra não comprova um banco relacional nem uma GUI real; não se deve afirmar isso apenas pelo README.

## Backup em cópia
- Origem: `dados-ensaio/sorveteria-ficticia.db` (dados artificiais).
- Destino: `dados-ensaio/sorveteria-ficticia-backup.db` (precisa não existir).
- Comando: `python backup_sqlite.py dados-ensaio/sorveteria-ficticia.db dados-ensaio/sorveteria-ficticia-backup.db`.
- Conferência: `python verificar.py` testa `PRAGMA integrity_check` e consulta IDs/nomes/valores conhecidos em outra conexão.
- Segurança: não restaurar por cima do banco principal; se o destino existir, a operação recusa e preserva seus bytes.

## Feedback e próxima ação para A20
Feedback real de colega/professor: preencher após a apresentação; não inventar.
Pendência selecionada para revalidar: inspeção manual da GUI e percurso por teclado/foco, ainda não comprovados pelos testes automatizados.
Teste A20: abrir a mesma versão A18 em desktop, executar o fluxo válido e a recusa/correção com dados fictícios, registrar o percurso Tab/Shift+Tab, mensagem, foco e redimensionamento; guardar evidência e feedback.
