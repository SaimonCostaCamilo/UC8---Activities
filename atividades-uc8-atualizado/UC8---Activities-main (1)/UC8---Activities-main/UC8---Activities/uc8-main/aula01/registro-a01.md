# A01 — minha tentativa e meus testes

**Nome:** Saimon Costa Camilo  
**Turma:** TDS  
**Data:** 05/11/2026


Use código de estudante na entrega. Não inclua dados pessoais de terceiros.

* Python observado: 313

* Tcl/Tk observado: integrado do python

* Interpretador selecionado no VS Code:

## Diagnóstico sem consulta
1. O que distingue texto de número? Se foi tratada ou não a entrada de dados.
2. Como uma função recebe uma entrada e produz uma saída? Recebe por parametros e utiliza 
3. O que uma condição decide?
Minha resposta inicial: Como serão tratados os dados 

## Matriz de testes (preencha antes e depois da execução)
| Nome fictício | Idade digitada | Resultado esperado | Resultado observado | Ajuste |
|---|---|---|---|---|
| Lia | 18 | Nome: Lia de idade 18| Nome: Lia de idade 18 | Tudo ok |
| vazio | 18 | Nome: de idade 18 | Nome: de idade 18 | Validação de nome preenchido|
| somente espaços | 18 |Nome:    de idade 18 |Nome: de idade 18    | validar entrada para evitar apenas espaços ou vazio |
| Lia | vazio | idade deve ser um numero inteiro maior que zero |idade deve ser um numero inteiro maior que zero |validação implementada |
| Lia | abc | idade deve ser um numero inteiro maior que zero| idade deve ser um numero inteiro maior que zero| validação implementada|
| Lia | 0 | idade deve ser maior que zero| idade deve ser maior que zero| validação implementada |
| Lia | -2 |idade deve ser maior que zero | idade deve ser maior que zero| validação implementada|
| Lia | 2.5 | erro de numero não inteiro  |idade deve ser maior que zero | implementar validação de floats|
| Ana Maria | 21 | Nome: Ana Maria de idade 21|Nome: Ana Maria de idade 21 | Tudo ok|

## Interface
Testei botão, Tab e Shift+Tab:
Comparei o resultado do terminal com o da janela:
Fechei e reabri; o que aconteceu com o resultado?
Resultado não persiste, como esperado

## Fechamento (sem consulta)
Explique entrada → validação → resposta com suas palavras:

* Entrada :captura de dados

* Validação: verificações lógicas de acordo com minhas RN feitas a partir de dados

* Resposta: Retorno oferecido de acordo com lógica implementada.

Uma dificuldade, a correção que tentei e meu próximo passo:

* Relembrar como usar tkinter

Arquivos anexados separadamente: terminal.py e cadastro.py.
