# Meu registro A19 — Academia e demonstrações individuais

**Nome:** Saimon Costa Camilo  
**Turma:** TDS  
**Data:** 17/11/2026

## Retomada sem consulta
- Demonstração: ação executada + resultado observado + limite.
- Backup válido: origem existente, destino novo, cópia via `Connection.backup()`, integridade e consulta conhecida.
- Preservação: não sobrescrever origem nem destino anterior; usar dados fictícios.

## Arquitetura antes do código
- `referencia-a18/modelos.py`: entidades e estado do pedido em memória.
- `referencia-a18/pagamento.py`: validação monetária e cálculo.
- `referencia-a18/repositorio.py`: persistência SQLite e transações.
- `referencia-a18/controller.py`: coordenação entre interface e repositório.
- `referencia-a18/main.py`: interface Tkinter.
- `backup_sqlite.py`: operação isolada de cópia de segurança.
- `verificar.py`: testes automatizados da operação de backup em arquivos temporários.

## Matriz de execução
### T01 — Demonstração apresenta execução e explicação próprias
**Previsão:** suíte A18 e ensaio lógico devem executar e exibir os casos previstos.  
**Observado:** `python -B verificar.py` em `referencia-a18/` terminou com código 0; `python -B ensaio-a18-logic.py` terminou com código 0.  
**Correção/reteste ou pendência:** roteiro preparado; apresentação individual ao vivo/feedback de colega ainda pendente.

### T02 — Fluxo válido, falha/cancelamento e persistência/relatório
**Previsão:** suíte deve cobrir persistência/reabertura, falha e exportação CSV.  
**Observado:** saída da suíte registrou T06 rollback da venda e itens, T07 reabertura e T09 CSV; todos OK.  
**Correção/reteste ou pendência:** inspeção ao vivo da interface e cancelamento pela GUI pendentes.

### T03 — Pergunta técnica individual
**Previsão:** justificar uma decisão com arquivos e teste.  
**Observado:** justificativa registrada em `roteiro-demo.md`: pedido em memória até confirmação e venda/itens na mesma transação.  
**Correção/reteste ou pendência:** explicar oralmente ao professor/colega e receber feedback.

### T04 — Academia: entidade, responsabilidade e armazenamento
**Previsão:** identificar entidades e IDs sem atribuir à amostra recursos não demonstrados.  
**Observado:** `academia_amostra.py` contém alunos 41/92, plano 7 e matrícula 101; funções JSON e consulta por ID.  
**Correção/reteste ou pendência:** discutir regra de exclusão do aluno vinculado; amostra não comprova GUI ou banco relacional.

### T05 — Backup com destino novo
**Previsão:** cópia consultável, integridade `ok`, origem intacta; destino existente recusado.  
**Observado:** `python -B verificar.py` executou os quatro cenários de backup em diretório temporário; todos os asserts passaram.  
**Correção/reteste ou pendência:** repetir CLI com os caminhos de ensaio locais em máquina do laboratório.

### T06 — Origem ausente
**Previsão:** `FileNotFoundError`, sem criar arquivo destino.  
**Observado:** teste passou; destino permaneceu inexistente.  
**Correção/reteste ou pendência:** nenhuma no teste automatizado; repetir no laboratório.

### T07 — Cópia íntegra e registros conhecidos
**Previsão:** `PRAGMA integrity_check` retorna `ok`; consulta retorna duas linhas exatas.  
**Observado:** assert passou para `(501, Lia Fictícia, 2350)` e `(502, Rui Fictício, 4100)`.  
**Correção/reteste ou pendência:** cópia temporária é removida ao fim do teste; ensaio manual CLI ainda deve ser executado no laboratório.

### T08 — Entrega sem ambientes/caches/dados reais
**Previsão:** ZIP contém fonte, documentação e referência A18; sem banco de produção ou cache.  
**Observado:** pacote A19 contém somente dados de teste gerados em tempo de execução; banco fictício não é distribuído.  
**Correção/reteste ou pendência:** conferir novamente após baixar/descompactar no computador de uso.

### T09 — Feedback e teste de recuperação
**Previsão:** registrar feedback real e escolher pendência objetiva para A20.  
**Observado:** pendência técnica selecionada: inspeção manual da GUI e navegação por teclado. Feedback externo ainda não recebido.  
**Correção/reteste ou pendência:** registrar comentário do colega/professor e revalidar GUI na A20.

## Explicação individual
Uma decisão que consigo justificar: separar montagem em memória da persistência confirmada; usar transação para que venda e itens sejam atômicos.  
Dificuldade/apoio/próxima tentativa: inspeção visual e de teclado exige desktop com ambiente gráfico; repetir com colega no laboratório.

## Arquivos e comandos
- Candidata: `referencia-a18/` (cópia preservada, sem alterações nesta A19).
- Testes A18: entrar em `referencia-a18/` e executar `python -B verificar.py` e `python -B ensaio-a18-logic.py`.
- Testes A19: executar `python -B verificar.py` na raiz da pasta A19.
- Banco fictício manual: `python preparar_ensaio.py`; depois executar o comando de backup documentado em `roteiro-demo.md`.
- Dados reais: não utilizados.

## Teoria e transferência
**Por que arquivo existente não basta?** A presença do arquivo não prova que ele abre, tem integridade ou contém os registros necessários.  
**Como foi conferido?** A cópia foi aberta por outra conexão, `PRAGMA integrity_check` retornou `ok` e a consulta comparou os registros conhecidos.  
**Por que destino novo?** Evita destruir uma cópia anterior e torna o resultado do ensaio rastreável.  
**Como se liga à candidata?** A candidata usa SQLite; o backup A19 usa a API própria do SQLite para copiar a base sem alterar a origem.

## Checklist da interface
- Controles/rótulos: não reavaliados visualmente nesta execução automatizada.
- Tab/Shift+Tab, foco e acionamento: pendente de inspeção manual.
- Mensagem após erro e possibilidade de corrigir: lógica automatizada A18 exercitada; mensagem visual ainda pendente.
- Redimensionamento: pendente.

## Pendências
- Feedback real de colega/professor ainda não coletado.
- Inspeção manual da GUI, teclado, foco e redimensionamento não comprovada por teste sem janela.
- Repetir o backup por CLI com os caminhos de ensaio na máquina de entrega.

## Para a A20
- Versão demonstrada: candidata A18 preservada em `referencia-a18/`.
- Evidência observada: suíte A14–A18 e ensaio lógico executados com código de saída 0; backup A19 validado por asserts.
- Pendência escolhida: inspeção manual da GUI e percurso por teclado/foco.
- Reteste esperado: reproduzir fluxo válido e erro/correção, conferir foco, mensagens, Tab/Shift+Tab e redimensionamento; registrar feedback e evidência.
