# A02 — estados e transições do cadastro

**Nome:** Saimon Costa Camilo  
**Turma:** TDS  
**Data:** 05/11/2026


Código do estudante:
Arquivo e interpretador executados:

## Retomada sem consulta
1. O que get devolve? Por que int pode falhar?



* Minha resposta inicial: Ele pega o valor do campo, por erro de casting

2. O que muda entre passar uma função e chamá-la ao ligar um botão?

* Minha resposta inicial: A chamada de função recebe os dados a serem tratados e a função ligada ao botão busca o estado dos campos então ela não associa inicialmente outros dados na chamada da função

3. Que caso detecta um nome preenchido somente com espaços?
* Minha resposta inicial: Uma validação em uma função utilizando strip

## Preveja e depois execute (nomes sempre fictícios)
| Caso | Estado/ação | Previsão | Observação | Ajuste |
|---|---|---|---|---|
| T01 | Abrir e Exibir antes de Registrar | Que apareça uma msg informando registros vazios| Registros:  | Colocar uma validação que retorne uma msg informando registros vazios |
| T02 | Registrar Lia / Costa / 18 e Exibir | Informar que os dados foram inseridos e limpar os campos | Funcionando como esperado |  Sem ajustes|
| T03 | Editar para Rui / Lima / 22; somente Exibir | Exibe apenas os valores registrados | Exibe os valores registrados | Poderia retornar os valores aos campos, mas teria problemas com multiplos registros|
| T04 | Limpar campos e depois Exibir | Limpa os campos e exibe em aviso a lista de registros | Executando como esperado | Poderia melhorar a saida de dados no aviso |
| T05 | Após um válido, tentar registrar outro nome com idade abc | Não deixa, aponta msg de que não pode ser adicionado | Resultado esperado ok|sem ajustes |
| T06 | Registrar Rui / Lima / 22; depois Exibir | Notifica o registro e e ao clicar em exibir passa a lista toda| comportamento esperado ok| sem alterações |
| T07 | Nome vazio ou somente espaços | Notifica o erro e não adiciona o registro | Funciona como esperado | Sem ajustes |
| T08 | Sobrenome vazio ou somente espaços |Notifica o erro e não adiciona o registro | Notifica o erro e não adiciona o registro | Sem ajustes |
| T09 | Idade vazia, 0, -2 e 2.5 (um teste por entrada) | Validação funcionando ok | validando entradas ok | sem ajustes adicionais |
| T10 | Espaços nas pontas e nome composto | Fazendo o strip() ok na validação | aplicando strip como esperado | sem ajustes |
| T11 | Fechar, reabrir e Exibir | Não mantem estado como esperado | Funcionando como esperado | sem ajustes |

## Uso da interface
Percorri campos e botões com Tab/Shift+Tab:

* Percorre mas não aplica as confirmações via teclado

Mensagem que precisei melhorar:

* Modifiquei algumas mensagens para ficar mais claro o que esta acontecendo ao usuário

Colega que testou (código fictício ou combinado): 

* tudo ok

## Fechamento sem consulta
Por que Limpar campos não deve apagar o registro confirmado? 

* Porque o registro deve ficar armazendo em uma lista independente dos campos 

Como uma tentativa inválida pode estragar um cadastro anterior se a ordem do código estiver errada?

* Se não tiver sido tratado o registro dos dados corretamente 

Minha dificuldade, ajuste e próximo passo:

* ainda relembrando como funciona o tkinter

Entregas externas: estado_cadastro.py e cadastro_completo.py, além deste registro.
