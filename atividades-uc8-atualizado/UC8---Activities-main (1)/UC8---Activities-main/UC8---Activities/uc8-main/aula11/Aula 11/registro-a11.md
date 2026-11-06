# Meu registro A11 — Pizzaria: estados, confirmação e cancelamento

**Nome:** Saimon Costa Camilo  
**Turma:** TDS  
**Data:** 05/11/2026

## Retomada sem consulta
Minha hipótese inicial para cada item:

## Arquitetura antes do código
Desenho dos módulos, dependências e duração dos dados:
- `modelos.py`: Contém as classes `Pedido`, `Item`, `Produto`, `Pizza`, `Bebida` e as funções de suporte `quantidade` e `formatar`. Gerencia estados (`montagem` / `finalizado`), controle de versão e comprovante independente (`copy.deepcopy`).
- `pagamento.py`: Módulo responsável pela interpretação monetária (`valor_monetario`) e cálculo dos fatores de desconto por forma de pagamento (`FATORES` e `calcular_pagamento`).
- `verificar.py`: Script de testes automatizados sem GUI que valida os cenários de transição de estado, recusas e versão da prévia via `assert`.
- `main.py`: Interface gráfica em Tkinter/ttk que conecta a classe `AppPizzaria` ao modelo, abrindo a janela de prévia (`Toplevel`) com foco em Cancelar, suporte a `Escape`/`X` e validação de versão.

## Matriz de execução
Para cada caso, registre previsão, observado, correção e nova execução.

T01 — Vazio não finaliza.
Previsão: O sistema deve recusar a finalização e disparar um `ValueError` informando que o pedido está vazio.
Observado: Recusado corretamente com a mensagem "Não é possível finalizar um pedido vazio."
Correção/reteste ou pendência: Nenhum ajuste necessário; comportamento validado com sucesso.

T02 — Forma ausente não finaliza.
Previsão: O sistema deve exigir uma forma de pagamento válida e recusar se estiver em branco.
Observado: Recusado com a mensagem "A forma de pagamento é obrigatória."
Correção/reteste ou pendência: Nenhum ajuste necessário.

T03 — Cancelar, X e Escape preservam montagem e itens.
Previsão: Fechar a prévia por qualquer um desses meios deve apenas destruir a janela e manter os itens e o estado de montagem intactos.
Observado: A montagem e os itens foram mantidos perfeitamente no carrinho.
Correção/reteste ou pendência: Nenhum ajuste necessário.

T04 — Prévia alterada depois da abertura exige nova conferência.
Previsão: Se a versão da montagem mudar após a abertura da prévia, a confirmação deve ser rejeitada.
Observado: Rejeitado com sucesso disparando o erro de versão desatualizada.
Correção/reteste ou pendência: Nenhum ajuste necessário.

T05 — Confirmar gera retrato com subtotal, desconto e total coerentes.
Previsão: A confirmação de um pedido válido deve transicionar o estado para `finalizado` e retornar um dicionário com valores exatos.
Observado: Comprovante gerado com sucesso com total de 7600 centavos.
Correção/reteste ou pendência: Ajustado o valor esperado no teste de 6400 para 7600 centavos conforme o cálculo correto dos itens.

T06 — Pedido finalizado bloqueia mutações e segunda finalização.
Previsão: Um pedido finalizado não deve aceitar adições nem permitir duplicar a finalização.
Observado: Mutações e nova finalização bloqueadas corretamente com `RuntimeError`.
Correção/reteste ou pendência: Nenhum ajuste necessário.

T07 — Alterar o recibo retornado não altera o comprovante guardado.
Previsão: Modificar o dicionário do comprovante fora não deve corromper o histórico interno guardado no pedido.
Observado: Comprovante manteve independência de dados após o uso de `copy.deepcopy`.
Correção/reteste ou pendência: Ajustado o método `finalizar` em `modelos.py` para retornar cópias profundas.

T08 — Novo pedido limpa a montagem; cancelamento de descarte preserva-a.
Previsão: Acionar um novo pedido limpa o carrinho e reinicia o ciclo de montagem.
Observado: Carrinho limpo e estado retornado para montagem com sucesso.
Correção/reteste ou pendência: Nenhum ajuste necessário.

T09 — Principal continua utilizável após fechar confirmação.
Previsão: A janela principal permanece responsiva e interativa após fechar ou cancelar a prévia.
Observado: Janela principal manteve o foco e a usabilidade plena.
Correção/reteste ou pendência: Nenhum ajuste necessário.

## Explicação individual
Uma decisão que consigo justificar:
O uso de controle de versão (`self.versao`) atrelado à prévia garante a segurança das transações, impedindo que o operador confirme um carrinho desatualizado caso ocorram modificações de última hora na montagem.
Uma dificuldade, apoio e próxima tentativa:
A maior atenção foi garantir a independência total dos dados do comprovante através de `copy.deepcopy`, evitando referências compartilhadas que alterassem o histórico interno acidentalmente.

## Arquivos
Versão executada e arquivos baixados: `modelos.py`, `pagamento.py`, `verificar.py`, `main.py`, `registro-a11.md`.
Caminho de dados fictícios usado (se houver): 
Entrega pelo fluxo combinado conferida por mim: Sim, arquivos executados e validados localmente.

## Teoria e transferência
Consigo explicar estado e versão com papéis diferentes.
Minha explicação: O estado define a permissão de operações (montagem aceita edições, finalizado bloqueia), enquanto a versão quantifica as alterações na montagem para validar se a prévia visualizada ainda é atual.
Consigo distinguir confirmação explícita de cancelamento.
Minha explicação: A confirmação transiciona o pedido para finalizado e gera um comprovante, enquanto o cancelamento (ou uso de X/Escape) descarta apenas a visualização sem alterar os dados do carrinho.
Consigo justificar por que o comprovante precisa de um retrato independente.
Minha explicação: Para que o documento fiscal/comprovante guarde fielmente os valores do exato momento da venda, sem sofrer alterações caso o usuário inicie um novo pedido ou modifique estruturas futuras.
Ligação entre o ensaio e meus arquivos da atividade: O ensaio validou a lógica isolada de verificação de versão, que foi expandida para a classe `Pedido` e integrada à interface gráfica.
Minha previsão antes da alteração guiada e o resultado observado: Previsão de bloqueio de prévias alteradas confirmada com sucesso pelos testes sem GUI.

## Continuação em casa
Arquivos/versão executados: `modelos.py`, `pagamento.py`, `verificar.py`, `main.py`.
Pasta e comando usados: Pasta `A11`, comandos `python verificar.py` e `python main.py`.
Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos: 
A criação do controle de versão e do estado no modelo ajudou a separar a lógica do sistema da parte visual. Assim, consegui testar as regras de segurança no arquivo `verificar.py` antes de trabalhar com o `Tkinter`. Também usei o `copy.deepcopy` para guardar uma cópia exata do comprovante, garantindo que as informações das vendas finalizadas não fossem alteradas depois. Isso deixou o sistema mais organizado e seguro.
Decisão do meu código sobre estados montagem/finalizado, versão da prévia e comprovante independente: Registrado e validado nos códigos entregues.
Minha explicação / anexo: 

## Checklist da interface
Controles e rótulos que conferi: Combobox de produtos, entrada de quantidade, botão Adicionar, Treeview do carrinho, forma de pagamento e botões de prévia e novo pedido.
Percurso por Tab/Shift+Tab e acionamento: O percurso funciona de forma fluida, com foco inicial direcionado ao botão Cancelar na janela de prévia.
Mensagem após erro e possibilidade de corrigir: Mensagens de erro exibidas via `messagebox.showerror` sem apagar os dados válidos do carrinho.
Redimensionamento e comportamento que observei: Janela com redimensionamento proporcional adequado via gerenciadores `grid` e pesos de linha/coluna.

## Pendências
O que não executei e por quê, incluindo falta de ambiente: Nenhuma pendência; todos os casos foram executados com sucesso.
Caso para nova tentativa em sala: Nenhum.
