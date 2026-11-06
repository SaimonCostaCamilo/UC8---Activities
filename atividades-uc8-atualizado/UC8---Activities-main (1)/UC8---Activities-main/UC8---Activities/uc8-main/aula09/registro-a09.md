# Meu registro A09 — Catálogo e carrinho: seleção por identidade

**Nome:** Saimon Costa Camilo  
**Turma:** TDS  
**Data:** 05/11/2026

## Retomada sem consulta
Minha hipótese inicial para cada item: O uso de índices numéricos para gerenciar linhas de tabelas visuais falha quando a interface sofre reordenações, sendo obrigatório o mapeamento por chaves únicas (IDs/iid) no modelo de dicionários.

## Arquitetura antes do código
Desenho dos módulos, dependências e duração dos dados: 

modelos.py: Gerencia a lógica central do carrinho usando um dicionário em memória indexado pelo código do produto (Produto, Item, Pedido), garantindo operações consistentes com Decimal.

pagamento.py: Módulo responsável pela interpretação monetária estrita (ROUND_HALF_UP) e cálculo de prévias de pagamento com fatores de desconto.

main.py: Interface gráfica em Tkinter contendo a árvore (ttk.Treeview), barras de rolagem, comboboxes de catálogo e pagamentos, além dos callbacks de CRUD.

## Matriz de execução
Para cada caso, registre previsão, observado, correção e nova execução.

T01 — Uma linha por código, repetição soma quantidade.
Previsão: Inserir o mesmo produto duas vezes deve incrementar a quantidade na mesma linha em vez de duplicá-la.
Observado: Quantidade acumulada corretamente no dicionário e na exibição.
Correção/reteste ou pendência: Nenhuma.

T02 — Atualizar fruta para quatro com leite três: total 42,50.
Previsão: O subtotal deve refletir exatamente a soma das quantidades multiplicadas pelos preços unitários.
Observado: Total calculado R$ 42,50.
Correção/reteste ou pendência: Nenhum.

T03 — Remover leite: total 20,00; remover fruta: zero.
Previsão: A remoção individual subtrai o subtotal do item correspondente até zerar o carrinho.
Observado: Subtotal atualizado corretamente para R$ 20,00 após remover o leite e para R$ 0,00 após esvaziar.
Correção/reteste ou pendência: Nennhum.

T04 — Selecionar ID após mover/ordenar linhas mantém o alvo correto.
Previsão: O uso de iid baseado no código do produto impede que a alteração de posição visual afete a operação.
Observado: O produto correto continuou sendo atualizado/removido mesmo após reordenação visual.
Correção/reteste ou pendência: Nenhum.

T05 — Adicionar sem seleção de catálogo: orientação, sem mutação.
Previsão: O sistema deve disparar exceção tratada e exibir mensagem de aviso sem corromper o estado.
Observado: Aviso em vermelho exibido na interface mantendo os dados intactos.
Correção/reteste ou pendência: Nenhum.

T06 — Atualizar/remover sem seleção de carrinho: orientação.
Previsão: Exigir seleção prévia na tabela e orientar o usuário caso nenhuma linha esteja selecionada.
Observado: Mensagem orientativa exibida corretamente quando tabela.selection() retorna vazio.
Correção/reteste ou pendência: Nenhum.

T07 — Quantidade inválida ou ID inexistente preserva pedido.
Previsão: Entradas com letras, valores negativos ou códigos errados devem ser rejeitadas sem limpar o carrinho.
Observado: Exceções capturadas e estado do pedido preservado.
Correção/reteste ou pendência: Nenhum.

T08 — Barra de rolagem, expansão, Tab e seleção no teclado.
Previsão: Navegação por teclado funcional com Tab/Shift+Tab e barra de rolagem acoplada corretamente à tabela.
Observado: Foco e rolagem operando conforme esperado.
Correção/reteste ou pendência: Nenhum.

T09 — Pagamento recalculado a partir do novo subtotal.
Previsão: Mudar a forma de pagamento ou alterar itens atualiza dinamicamente a prévia líquida.
Observado: Valores recalculados automaticamente com arredondamento seguro (ROUND_HALF_UP).
Correção/reteste ou pendência: Nenhum.

## Explicação individual
Uma decisão que consigo justificar: Utilizar o código do produto como iid no Treeview garante que a interface e o modelo dialoguem com precisão, evitando bugs clássicos de manipulação baseada em índices mutáveis.
Uma dificuldade, apoio e próxima tentativa: Sincronizar o estado vazio da árvore visual sem disparar exceções de seleção automática. Documentação do Tkinter e tratamento explícito do estado com verificação de nós filhos. Expandir os testes de acessibilidade por teclado para novos componentes de formulário.

## Arquivos
Versão executada e arquivos baixados: modelos.py, pagamento.py, main.py, verificar.py.
Caminho de dados fictícios usado (se houver): Não
Entrega pelo fluxo combinado conferida por mim: Sim

## Teoria e transferência
Consigo distinguir identidade de posição visual.
Minha explicação: Posição visual é o índice dinâmico (linha 1, linha 2) que pode mudar com ordenações. Identidade é o código único (iid) atrelado ao registro do produto no dicionário do modelo.
Consigo explicar a diferença entre adicionar, atualizar e remover.
Minha explicação: Adicionar soma quantidades ao produto existente ou cria um novo registro, atualizar substitui diretamente a quantidade por um novo valor informado, remover elimina completamente a chave correspondente do dicionário.
Consigo prever a tela e o total ao remover o último item.
Minha explicação: A tabela fica totalmente limpa (sem linhas), o total geral do pedido retorna instantaneamente a R$ 0,00 e a prévia de pagamento zera, sem que a aplicação tente buscar seleções inexistentes.
Ligação entre o ensaio e meus arquivos da atividade: O ensaio demonstrou isoladamente que atualizar substitui valores e remover afeta apenas a chave indicada, o que foi aplicado diretamente nos métodos de dicionário do modelos.py.
Minha previsão antes da alteração guiada e o resultado observado: A integração das callbacks de ID na interface graphica exigiria tratamento de exceções para seleções vazias. O observado confirmou o funcionamento do programa após implementar as verificações.

## Continuação em casa
Arquivos/versão executados: main.py
Pasta e comando usados: Executado via ambiente de desenvolvimento local Python no diretório do projeto.
Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos:
A estruturação modular permitiu separar claramente as regras monetárias do layout visual. O uso do dicionário garantiu complexidade constante nas buscas por ID. A interface manteve-se resiliente a erros de entrada graças ao isolamento de exceções nos callbacks.
Decisão do meu código sobre identidade por código, iid/seleção, atualização/remoção e total derivado do modelo:
Minha explicação / anexo:
O sistema mapeia cada linha da interface diretamente para a chave do dicionário do pedido através do iid, garantindo que atualizações e remoções operem sobre a identidade inequívoca do produto, enquanto o total é derivado matematicamente do somatório dos sub-totais dos itens.

## Checklist da interface
Controles e rótulos que conferi: Comboboxes de catálogo/pagamento, campos de quantidade, Treeview com barra de rolagem, botões de ação e rótulos de totais e avisos.
Percurso por Tab/Shift+Tab e acionamento: Funcionando
Mensagem após erro e possibilidade de corrigir: Mensagens de erro exibidas em destaque visual claro, permitindo ao usuário corrigir o dado na mesma sessão sem reiniciar.
Redimensionamento e comportamento que observei: Janela dimensionada de forma responsiva com grades expansíveis (sticky="nsew").

## Pendências
O que não executei e por quê, incluindo falta de ambiente:
Caso para nova tentativa em sala:
