# Meu registro A10 — Pizzaria: transferir o modelo de pedido

**Nome:** Saimon Costa Camilo  
**Turma:** TDS  
**Data:** 05/11/2026

## Retomada sem consulta
Minha hipótese inicial para cada item:

## Arquitetura antes do código
Desenho dos módulos, dependências e duração dos dados:
- Módulos: `modelos.py` (contém Produto, Pizza, Bebida, Item, Pedido),`pagamento.py` (cálculo de descontos com `Decimal`), `verificar.py`(testes automatizados com `assert`) e `main.py`(interface em `Tkinter/tkk`).

- Dependências: `main.py` importa de `modelos.py` e `pagamento.py`.
`verificar.py` importa de `modelos.py`.

- Duração dos dados: Os dados do pedido existem apenas em memória durante a execução da sessão e são limpos ao fechar a janela.

## Matriz de execução
Para cada caso, registre previsão, observado, correção e nova execução.

T01 — Mussarela média 35,00 +dois refrigerantes 6,00: total 47,00.
Previsão:O sistema deve calcular exatamente 4700 centavos (R$ 47,00) ao somar 1 pizza média de 3500 e 2 bebidas de 600.
Observado:Total calculado e formatado perfeitamente como R$ 47,00.
Correção/reteste ou pendência:Nenhum ajuste necessário, comportamento validado por `assert`.

T02 — Pizza com tamanho desconhecido: recusar.
Previsão:O construtor da classe `Pizza`deve disparar um `ValueError` ao receber um tamanho fora do conjunto permitido("Média", "Grande").
Observado:Exceção capturada com sucesso, impedindo a criação do objeto inválido.
Correção/reteste ou pendência:Teste bem-sucedido.

T03 — Bebida e pizza coexistem com IDs distintos.
Previsão:O dicionário interno do pedido deve armazenar itens de classes diferentes (Pizza e Bebida) sem conflito, desde que usem códigos (codigo) distintos.
Observado:Os itens coexistiram no carrinho e foram listados corretamente na interface.
Correção/reteste ou pendência:Aprovado.

T04 — Atualizar/remover preserva alvo por ID.
Previsão:As operações de atualizar quantidade e remover item devem localizar exatamente o registro correto pelo código informado na seleção da tabela.
Observado:Apenas o item selecionado foi atualizado ou removido.
Correção/reteste ou pendência:Aprovado.

T05 — Quantidades inválidas mantêm o pedido anterior.
Previsão:Se uma quantidade inválida ("abc" ou número negativo) for informada, o sistema deve recusar com exceção e preservar intactos os itens anteriores do pedido.
Observado:O pedido permaneceu inalterado após a falha graças à interrupção segura da operação.
Correção/reteste ou pendência:Aprovado.

T06 — Pagamento usa as mesmas regras da A08, sem desconto acumulado.
Previsão:O módulo `pagamento.py` deve aplicar o fator correto (ex: PIX = 0.87) sobre o subtotal sem aplicar descontos duplicados.
Observado:Cálculo do pagamento efetuado seguindo estritamente as regras de fatores.
Correção/reteste ou pendência:Aprovado.

T07 — Comparação de eventos não duplica o modelo nem exige migração.
Previsão:A simulação de eventos externos demonstra que o núcleo da aplicação permanece independente de qual toolkit gerou a ação.
Observado:Lógica isolada com sucesso.
Correção/reteste ou pendência:Aprovado.

T08 — Demonstração opcional informa ausência da biblioteca sem instalar nada.
Previsão: O laboratório sem PySimpleGUI mantém o núcleo em ttk rodando normalmente.
Observado:Sistema executado com sucesso em Tkinter/ttk.
Correção/reteste ou pendência:Aprovado.

## Explicação individual
Uma decisão que consigo justificar:
Utilizar composição na classe `Pizza` e `Bebida` para compartilhar os dados comuns exigidos pelo `Item` (código, nome e preço em centavos), evitando duplicação de código e heranças desnecessárias.
Uma dificuldade, apoio e próxima tentativa:
A principal dificuldade inicial foi garantir que a conversão de quantidades e preços tratasse corretamente strings da interface sem quebrar o estado do pedido. O apoio veio da reutilização do validador baseado em `Decimal` e funções auxiliares.

## Arquivos
Versão executada e arquivos baixados:
`modelos.py, pagamento.py, verificar.py, main.py, registro-a10.md`
Caminho de dados fictícios usado (se houver):
Entrega pelo fluxo combinado conferida por mim:

## Teoria e transferência
Consigo separar o que mudou do que foi reutilizado.
Minha explicação:
Sim. O que mudou foi a introdução da validação de tamanho nas pizzas; o que foi reutilizado foi toda a lógica estrutural de carrinho, itens, quantidades e subtotais da A09.
Consigo explicar composição apontando a referência entre objetos.
Minha explicação:
A classe `Item` armazena uma referência direta ao objeto do produto (`self.produto = produto`)
Consigo mostrar como código/tamanho/preço chegam ao pedido.
Minha explicação:
Sim. O usuário seleciona o produto na interface, cujos atributos (incluindo o tamanho da pizza) são validados e passados ao método `adicionar` do `Pedido`.
Ligação entre o ensaio e meus arquivos da atividade:
O ensaio demonstrou que objetos diferentes podem compartilhar uma base comum, exatamente como `Pizza` e `Bebida` compartilham atributos com o `Item`.
Minha previsão antes da alteração guiada e o resultado observado: 

## Continuação em casa
Arquivos/versão executados:
Pasta e comando usados:
Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos:
A mudança da sorveteria para a pizzaria mostrou como a organização do código facilita fazer alterações sem precisar refazer tudo. Como a parte dos preços e dos itens ficou separada em `modelos.py`, foi possível adicionar características da pizza, como o tamanho, sem precisar mudar o funcionamento do carrinho. Com isso, entendi melhor como a orientação a objetos ajuda a organizar o código e como separar as responsabilidades deixa o projeto mais fácil de manter e modificar.
Decisão do meu código sobre transferência Produto/Pizza/Bebida, composição e contrato do pedido:
Adoção de classes enxutas que cumprem estritamente o contrato esperado pelo `Item`.

## Checklist da interface
Controles e rótulos que conferi:
Catálogo de produtos (`Combobox`), campo de quantidade (`Entry`), tabela de itens (`Treeview`), rótulo de total e seletor de formas de pagamento.
Percurso por Tab/Shift+Tab e acionamento:
Navegação fluida entre os campos de entrada e botões de ação utilizando o teclado.
Mensagem após erro e possibilidade de corrigir:
Exibição de caixas de diálogo de erro (`messagebox.showerror`) que permitem ao usuário corrigir os dados imediatamente sem perder o carrinho.
Redimensionamento e comportamento que observei:
Janela expansível com grades bem distribuídas utilizando gerenciamento `sticky="nsew"`.

## Pendências
O que não executei e por quê, incluindo falta de ambiente:Nenhuma pendência crítica; todo o núcleo em `ttk` e os testes foram executados com sucesso.
Caso para nova tentativa em sala:
