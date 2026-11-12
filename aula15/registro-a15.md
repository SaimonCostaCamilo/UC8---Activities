# Registro A15 — CRUD de produtos e início de clientes

**Nome:** Saimon Costa Camilo  
**Turma:** TDS  
**Data:** 12/11/2026  
**Dados:** todos os registros de teste são fictícios e os testes usam bancos temporários.

## Retomada e arquitetura

- `modelos.py`: `Produto`, `Item` e `Pedido` mantêm produtos do pedido, quantidades, subtotais e total em memória. O total é calculado pelo modelo, não por rótulos da janela.
- `pagamento.py`: interpretação monetária decimal, cálculo por forma de pagamento e conversão para centavos.
- `arquivos.py`: validação e leitura/escrita segura do catálogo JSON.
- `relatorios.py`: exportação CSV baseada no comprovante confirmado.
- `perfis.py`: sessão fictícia; selecionar Administração não comprova identidade real.
- `repositorio.py`: regras de validação e SQL SQLite; os dados de produtos/clientes persistem.
- `main.py`: janela Tkinter, campos, tabelas e callbacks. O pedido continua apenas em memória.
- `verificar.py`: testes automatizados sem abrir janela.

## Previsões antes da execução

1. Com dois produtos, editar um deles pelo ID deve deixar exatamente duas linhas: só nome e preço daquele ID mudam.
2. Clicar em **Novo** limpa seleção/campos e faz Salvar inserir um terceiro ID; não reaproveita o ID em edição.
3. Cancelar a exclusão mantém quantidade, registro e tabela sem alteração.
4. Confirmar remove apenas o ID selecionado. Excluir o último registro produz lista vazia válida.
5. ID inexistente retorna `False`; não deve produzir mensagem de sucesso nem criar cadastro.
6. Cliente fictício inserido deve aparecer na listagem e continuar após reabrir o arquivo SQLite.

## Matriz de execução automatizada

Comando executado: `python -B verificar.py` na pasta `A15`.

| Caso | Previsão | Observado | Resultado |
|---|---|---|---|
| T01 — editar mesmo ID | Atualiza nome/preço sem INSERT | Duas linhas permaneceram; ID alvo recebeu nome e 1300 centavos | PASSOU |
| T02 — reordenar e editar | Identidade vem do ID, não da posição | Lista invertida; edição posterior alterou o ID guardado | PASSOU |
| T03 — entrada inválida | Valor persistido anterior permanece | `ValueError`; nome anterior continuou no banco | PASSOU |
| T04 — ID inexistente | Nenhuma linha criada/alterada | `editar_produto(9999, ...)` retornou `False` | PASSOU |
| T05 — excluir sem seleção | Interface deve pedir seleção | Callback da interface implementado; GUI não executada neste ambiente | PENDENTE GUI |
| T06 — cancelar exclusão | Banco/lista preservados | `confirmado=False` retornou `False`; duas linhas preservadas | PASSOU (repositório) |
| T07 — confirmar exclusão | Só ID alvo removido | Exclusão confirmada removeu somente o ID indicado | PASSOU |
| T08 — lista vazia | Estado válido, sem exceção | Após excluir o último ID, consulta retornou `[]`; reabertura também `[]` | PASSOU |
| T09 — clientes | Inserir/listar e persistir | Cliente fictício reapareceu após reabrir banco | PASSOU |
| T10 — reabrir banco | Edição/exclusão gravadas persistem | Estado confirmado foi consultado por nova instância do repositório | PASSOU |

Também foram repetidos os testes de regressão A14 T00–T13, incluindo modelo do pedido, pagamento, JSON, CSV e perfil: todos passaram.

## Dificuldade, correção e reteste

Dificuldade investigada: a edição não pode depender do índice visual da linha, pois a ordenação muda a posição. A correção foi manter o ID como `iid` do `Treeview` e executar `UPDATE ... WHERE id = ?`; o repositório retorna `rowcount == 1` para distinguir ID existente de inexistente. O caminho de edição não chama `INSERT`. Nova execução: T14–T16 passaram e a contagem de linhas permaneceu constante durante a edição.

## Justificativa individual (rascunho de 5–8 linhas)

A edição usa `UPDATE` com `WHERE id = ?`, porque o ID é a identidade estável do cadastro.  
A posição visual da linha pode mudar quando a tabela é ordenada, por isso ela não identifica o produto.  
O botão Novo limpa a seleção e troca explicitamente o modo para inclusão; Salvar então usa INSERT.  
No modo editar, Salvar exige uma seleção e atualiza o mesmo ID, sem duplicar a linha.  
Excluir primeiro identifica o ID e mostra nome e código na confirmação.  
Cancelar não chama o DELETE; somente a confirmação explícita autoriza a exclusão.  
Clientes começam com inclusão/listagem de nomes fictícios, enquanto o pedido permanece em memória.

## Checklist da interface — preencher após executar em desktop

- Controles/rótulos conferidos: **pendente**
- Tab/Shift+Tab e acionamento pelo teclado: **pendente**
- Mensagem após erro e correção na mesma sessão: **pendente**
- Redimensionamento e comportamento da janela: **pendente**
- Testes GUI de Novo, edição, cancelamento, lista vazia e clientes: **pendente**

**Limite da execução:** os testes automatizados foram executados. A janela Tkinter não foi aberta nesta execução automatizada; portanto, não declarar testes visuais/teclado como realizados. Execute `python main.py` em um computador com ambiente gráfico para completar o checklist.
