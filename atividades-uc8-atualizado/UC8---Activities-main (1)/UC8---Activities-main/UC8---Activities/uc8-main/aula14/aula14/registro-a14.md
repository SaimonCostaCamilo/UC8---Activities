# Meu registro A14 — SQLite: produtos que permanecem após reabrir

Nome: Saimon  
Turma: TDS  
Data: 09/11/2026

## Retomada sem consulta

- A função `iniciar()` cria as tabelas com `CREATE TABLE IF NOT EXISTS`, sem apagar registros.
- `adicionar_produto()` valida os campos, converte preço para centavos e usa `?` com uma tupla de parâmetros.
- `commit()` confirma a gravação; `closing()` garante o fechamento da conexão.
- `listar_produtos()` consulta o arquivo persistente; o ID do banco é a identidade do produto, não a posição da linha na tela.
- O pedido continua sendo calculado por `Pedido.total_centavos()` a partir dos subtotais dos itens em memória.

## Arquitetura antes do código

`main.py` (interface) → `repositorio.py` (SQLite) → arquivo `dados/mercado.db`.

A interface também utiliza `modelos.py` para produto/pedido. `pagamento.py`, `arquivos.py`, `relatorios.py` e `perfis.py` preservam as responsabilidades já desenvolvidas nas aulas anteriores. O banco dura entre execuções; a montagem do pedido dura somente enquanto o programa está aberto.

## Matriz de execução — testes automatizados

Os resultados abaixo foram observados pela execução de `python verificar.py` em ambiente Python. Os casos são dados fictícios e foram executados com diretórios temporários, sem reutilizar um banco pessoal.

| Caso | Previsão | Observado | Resultado |
|---|---|---|---|
| T00 — Importar/construir repositório | Não cria banco automaticamente | Arquivo não existia após importação e construção | Aprovado |
| T01 — Criar tabelas novamente | Não apagar produtos existentes | Produto permaneceu após segunda inicialização | Aprovado |
| T02 — Preço `7,50` | Armazenar inteiro `750` | Registro retornou `preco_centavos = 750` | Aprovado |
| T03 — Nome `D'água` | Apóstrofo tratado como dado literal | Nome foi gravado e consultado sem erro | Aprovado |
| T04 — Nome vazio/preço inválido/zero | Recusar sem inserir linha | Exceções `ValueError`; lista permaneceu igual | Aprovado |
| T05 — IDs positivos únicos | ID não depende da posição visual | IDs `1`, `2`, `3`, sem repetição | Aprovado |
| T06 — Reabrir o mesmo caminho | Produtos permanecem no banco | Nova instância consultou os mesmos registros | Aprovado |
| T07 — Falha de conexão | Não anunciar sucesso nem alterar banco válido | Erro SQLite propagado; banco válido permaneceu igual | Aprovado |
| T08 — Validação monetária | Converter reais em centavos e rejeitar texto inválido | Conversões e recusas conferidas por `assert` | Aprovado |
| T09 — Pedido em memória | Total calculado pelos subtotais do modelo | Adição, atualização e remoção conferidas | Aprovado |
| T10 — Sair do perfil | Limpar sessão, sem apagar pedido | Nome/perfil limpos; total do pedido preservado | Aprovado |
| T11 — JSON | Distinguir ausente de inválido sem sobrescrever origem | Ausente retornou lista vazia; inválido gerou erro e permaneceu intacto | Aprovado |
| T12 — CSV | Exportar o comprovante confirmado | CSV reaberto com nome especial, subtotal e BOM UTF-8 | Aprovado |
| T13 — Clientes | Persistir usando parâmetros | Cliente com apóstrofo gravado e consultado | Aprovado |

**Comando executado:** `python verificar.py`  
**Saída observada:** `Todos os casos automatizados A14 foram aprovados.`

## Correção e reteste

A implementação de persistência foi estruturada para não limpar os campos antes da confirmação do banco. O caminho de erro foi coberto por testes de validação e falha de conexão: o método não retorna registro de sucesso quando a gravação falha, e os registros válidos anteriores continuam consultáveis. O reteste automatizado passou.

## Explicação individual — texto-base para revisar com suas palavras

O repositório separa a instrução SQL dos valores usando placeholders `?` e uma tupla de parâmetros. Isso permite gravar nomes com apóstrofos sem transformar o conteúdo em comando SQL. O preço é convertido para centavos inteiros antes da gravação, evitando imprecisão de ponto flutuante. Depois do `INSERT`, a transação é confirmada com `commit()` e a conexão é fechada. A interface só limpa os campos e atualiza a lista depois que o método retorna com sucesso. O banco conserva produtos entre execuções, enquanto o pedido desta aula permanece em memória.

## Checklist da interface — validação manual pendente

- [ ] Abrir a janela com `python main.py` em ambiente com Tkinter.
- [ ] Cadastrar produto com nome comum e preço `7,50`; confirmar ID, nome e preço na tabela.
- [ ] Cadastrar `D'água`; confirmar que o apóstrofo é preservado.
- [ ] Tentar nome vazio e preço inválido; conferir mensagem e permanência dos campos.
- [ ] Fechar e reabrir o programa; conferir que os produtos continuam listados.
- [ ] Selecionar produto e adicioná-lo ao pedido; conferir que o total vem do modelo.
- [ ] Conferir navegação por Tab/Shift+Tab, foco, mensagens e redimensionamento.

Esses itens dependem de interação visual e **não foram marcados como executados** pelo teste automatizado sem GUI.

## Teoria e transferência

- **SQLite:** adequado para dados estruturados que precisam continuar disponíveis após encerrar o programa.
- **JSON:** adequado para catálogo/configuração simples em arquivo, com validação do conteúdo.
- **CSV:** adequado para exportar relatórios tabulares e compartilhar dados.
- **Memória:** adequada para o estado temporário do pedido durante esta etapa do projeto.

## Pendências

1. Conferir manualmente a interface Tkinter e preencher o checklist acima.
2. Preencher nome, turma e data.
3. Rever o texto-base da explicação e adaptá-lo à explicação individual do aluno.
4. Realizar a entrega no OneDrive pelo fluxo indicado no enunciado; o envio externo não é executado por este pacote.
