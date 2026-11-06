# A03 — testes do conversor fictício

**Nome:** Saimon Costa Camilo  
**Turma:** TDS  
**Data:** 05/11/2026


Código do estudante:
Arquivo e interpretador executados:

## Retomada sem consulta
O que Exibir deve ler quando os campos foram editados sem confirmação?

Minha resposta inicial: Nenhum registro encontrado

Por que um erro não pode alterar parte do último registro válido?

Minha resposta inicial: Por causa dos tratamentos feitos em calcular

O que get devolve? Por que int não serve para uma idade escrita como 2.5?

Minha resposta inicial: Get devolve o conteudo do campo de mesmo nome. 2.5 é float, int não irá comportar o valor corretamente.

## Antes de programar
Unidade das cotações: float

Operação escolhida para converter reais; justificativa por unidades: cast float com casa decimal formatada

Quais entradas e resultados precisam pertencer à mesma tentativa? Entrada e resultados do mesmo registro validado

## Preveja e depois execute
As cotações desta tabela são fictícias. Mantenha a ordem quando o caso indicar.
| Caso | Entrada/ação | Previsão | Observação | Ajuste |
|---|---|---|---|---|
| T01 | Abrir e Exibir antes de Calcular | Exibir msg de registro vazio | Previsão mantida | Nenhum |
| T02 | Calcular reais 100, cotação USD 5 e EUR 4 | Exibir os valores convertidos em string formatada | Armazenar o resultado da conversão em uma lista| sem ajustes |
| T03 | Editar para 200 / 10 / 8; somente Exibir | Exibir os registros calculados| Irá manter os valores nos campos, mas exibir os valores registrados corretamente | Poderia limpar os campos ao clicar em exibir, mas não é necessário e teria que se questionar a validade |
| T04 | Após T02, Calcular com 200 / 10 / abc | Exibe msg de erro ao calcular e não salva| Valida e não salva o calculo com erro | sem ajustes |
| T05 | Corrigir para 200 / 10 / 8 e Calcular | Valida e insere nos registros  | comportamento esperado ok | sem ajustes |
| T06 | Calcular com 100,50 / 5 / 4; repetir com 100.50 | Registra os dois sem problemas | Como esperado | sem ajustes |
| T07 | Calcular com 0 / 5 / 4 | Erro na validação, não salva | como esperado | sem ajustes |
| T08 | Reais negativos; cada cotação 0 e negativa, um teste por campo | Valida e não salva | valida e não salva |  sem ajustes |
| T09 | Cada campo vazio, só espaços ou abc, um por vez | Campos vazios não aceitos | valida e não aceita,informa erro | sem ajustes |
| T10 | Texto 1.000,50 ou 1,000.50; depois 1000,50 sem milhares | deve inserir sem problemas | aponta erro na validação | inseri o ('.', '').replace(',', '.') para tratar a entrada de dados |
| T11 | Após um válido, Limpar campos e depois Exibir | Insere, limpa e exibe a lista de registros salvos| funciona como esperado | sem ajustes |
| T12 | Calcular com 10 / 3 / 6; observar arredondamento de exibição | arredonda por .2f sem erros | como esperado | sem ajustes |
| T13 | Fechar, reabrir e Exibir | Não guarda a lista | como esperado |sem ajustes |

## Uso da interface
Percorri campos e botões com Tab/Shift+Tab:

Funciona como esperado

Usei o teclado para acionar um botão:

Não funciona ainda

Mensagem que precisei melhorar:

Modifiquei as mensagens de validação e entrada 

Colega que testou (código combinado): Ao inserir o valor de 6.9 está convertendo para 69.00. Voltei para a solução anterior, não aceita valores como 1.000,50 porque seria necessario tratar os dados e ficaria muito extensivo para este exercicio. Tratar a entrada de cada campo adicionaria muitas linhas ou precisaria de uma função.

## Fechamento sem consulta
Por que a cotação precisa ser maior que zero, mas o valor em reais pode ser zero?

* Nenhum deles deveria ser zero, mas nesse cenário causaria ZeroDivisionError.

Como evitar mostrar uma entrada atual com um resultado anterior? 

* Limpando os campos apos a inserção.

Formatar com duas casas muda o número guardado no registro?

* Se a entrada no registro for do dado formatado sim.


Minha dificuldade, correção e próximo passo:

* Lembrar melhor o funcionamento do tkinter

Entregas: calculos_moedas.py, conversor.py e este registro preenchido.

## Teoria e transferência

Consigo explicar por que a operação usa divisão.

Minha explicação: Porque é a formula da conversão de moedas.

Consigo distinguir normalização, conversão e formatação.

Minha explicação: Normalizar padroniza o dado, conversão faz a lógica de conversão do valor e a formatação a apresentação do dado armazenado

Consigo indicar quais dados devem ser confirmados juntos.

Minha explicação: Todos os campos devem ser confirmados antes de salvar para não ter erros nos dados

Ligação entre o ensaio e meus arquivos da atividade: Direta, os exercícios são baseados no material de aula

Minha previsão antes da alteração guiada e o resultado observado:

## Continuação em casa
Arquivos/versão executados:
Pasta e comando usados:
Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos:
Decisão do meu código sobre unidades, conversão decimal, aproximação de float e confirmação conjunta das cinco chaves:
Minha explicação / anexo:

## Checklist da interface
Controles e rótulos que conferi:
Percurso por Tab/Shift+Tab e acionamento:
Mensagem após erro e possibilidade de corrigir:
Redimensionamento e comportamento que observei:

## Pendências
O que não executei e por quê, incluindo falta de ambiente: 

Tudo testado e executado conforme mencionado nos testes acima. 

Caso para nova tentativa em sala: Tudo testado, tudo ok.
