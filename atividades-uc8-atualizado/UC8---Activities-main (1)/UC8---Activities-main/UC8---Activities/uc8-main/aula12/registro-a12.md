# Meu registro A12 — Mercado: navegação e catálogo em JSON

**Nome:** Saimon Costa Camilo  
**Turma:** TDS  
**Data:** 05/11/2026

## Retomada sem consulta
- JSON representa dados, não objetos Python vivos.
- Um arquivo ausente pode retornar uma lista vazia sem ser criado.
- JSON inválido e arquivo ausente são situações diferentes.
- Validar estrutura é diferente de apenas decodificar JSON.
- Gravação segura valida primeiro e substitui o destino somente depois de concluir a escrita temporária.

## Arquitetura antes do código
- `modelos.py`: classes e estado do pedido, reutilizados da A11 e aplicados aos pedidos do mercado.
- `pagamento.py`: interpretação monetária com Decimal, fatores e conversão para centavos, reutilizados da A11.
- `arquivos.py`: validação, leitura UTF-8 e gravação atômica do catálogo.
- `verificar.py`: testes sem interface e com diretório temporário.
- `main.py`: uma única janela Tk, Notebook com abas Pedido e Exercício JSON, menu de navegação.
- Duração dos dados: pedido do mercado permanece na instância da aplicação; texto JSON permanece no editor; arquivo só é criado em ação explícita de salvar.

## Matriz de execução

| Caso | Previsão | Observado | Correção/reteste |
|---|---|---|---|
| T01 — Ausente | Retorna `[]` sem criar arquivo. | Aprovado no teste automatizado. | Não necessária. |
| T02 — UTF-8 | Acentos são preservados na gravação/leitura. | Aprovado com “Picolé de limão”. | Não necessária. |
| T03 — JSON malformado/encoding inválido | Falha informada e bytes originais preservados. | Aprovado comparando bytes antes/depois. | Não necessária. |
| T04 — Estrutura inválida | Lista, chaves, IDs únicos/positivos, nome e preço são validados. | Aprovado para duplicidade, ID zero, preço zero, nome vazio e tipo incorreto. | Não necessária. |
| T05 — Falha de escrita | Destino anterior não deve ser substituído por dados inválidos. | Aprovado; arquivo existente manteve os bytes após falha simulada de `os.replace`, e o temporário foi removido. | Não necessária. |
| T06 — Cancelar seletor | Nenhuma alteração no editor/arquivo e sem sucesso anunciado. | Implementado por retorno imediato se caminho vazio; requer conferência manual da GUI. | Conferir no desktop. |
| T07 — Navegação | Pedido permanece na mesma instância entre abas. | A instância única é mantida no código; regressão do modelo passou. | Conferir visualmente no desktop. |
| T08 — JSON independente | Carregar/validar catálogo não altera carrinho. | Aprovado com comparação do estado do pedido antes/depois. | Não necessária. |

## Explicação individual
Uma decisão que consigo justificar: a gravação usa arquivo temporário no mesmo diretório e `os.replace` somente depois da escrita completa. Isso reduz o risco de deixar o catálogo de destino parcialmente escrito. A leitura não captura erro de JSON como se fosse arquivo ausente, pois são situações diferentes. Também corrigi um detalhe herdado no pagamento: o sinal negativo não pode ser removido pela limpeza do texto antes da validação.

Uma dificuldade, apoio e próxima tentativa: conferir visualmente o cancelamento dos seletores e a navegação na interface Tkinter. Próxima tentativa: executar `python main.py`, montar um pedido, alternar abas, cancelar os dois seletores e verificar que o carrinho e o editor permanecem iguais.

## Arquivos
- Versão executada: `arquivos.py`, `pagamento.py`, `modelos.py`, `verificar.py`, `main.py`.
- Dados fictícios: diretório temporário criado pelos testes; a interface não cria JSON ao iniciar.
- Entrega pelo fluxo combinado: conferir após executar localmente.

## Decisão técnica
O programa distingue arquivo ausente de arquivo que não pôde ser interpretado: `FileNotFoundError` retorna lista vazia; JSON malformado e encoding inválido geram erro. Portanto, não transforma uma falha de leitura em catálogo vazio e não sobrescreve o arquivo original.

## Pendências
- Executar a interface gráfica no computador e observar visualmente T06 e T07.
- A confirmação final do fluxo visual depende da execução local em ambiente com Tkinter.
