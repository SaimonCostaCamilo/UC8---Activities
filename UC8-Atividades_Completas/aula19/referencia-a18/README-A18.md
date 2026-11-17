# A18 — Regressão, correções e README reproduzível

**Projeto:** Sorveteria — candidata desktop para continuidade na A19  
**Responsável:** Saimon Costa Camilo · **Turma:** TDS · **Data:** 13/11/2026

## 1. Objetivo e limites

Esta pasta é uma cópia candidata baseada na versão A17. Ela mantém a regra central: **cadastros e vendas confirmadas são persistidos no SQLite; a montagem de um pedido ainda não confirmado existe somente em memória**. A venda e seus itens são gravados na mesma transação; se qualquer etapa falhar, o rollback evita uma venda parcial e o pedido continua aberto.

A correção guiada desta aula reforça a validação da quantidade e a entrada monetária. Uma quantidade inválida (por exemplo, `0`) não altera a montagem existente. Depois do erro, a pessoa pode informar `1` e atualizar o item. A interface ganhou a ação **Atualizar qtd.** para executar esse fluxo sem apagar o pedido. O parser monetário também deixou de remover letras silenciosamente: textos como `abc10` agora são recusados, em vez de serem convertidos em `10`.

A sessão de perfil continua sendo uma simulação local, não autenticação real. Os testes automatizados não abrem a janela e não usam o banco padrão: criam arquivos temporários isolados.

## 2. Ambiente

- Python 3.10 ou superior.
- Tkinter para abrir a interface gráfica.
- SQLite e demais módulos usados são da biblioteca padrão do Python.
- Não há dependências externas obrigatórias.
- `customtkinter` é opcional e usado apenas por `comparar_ctk.py`.

Ambiente em que a suíte foi executada nesta entrega: **Python 3.13.5**, Tcl/Tk 8.6. A importação do Tkinter foi conferida; a inspeção visual da janela ainda precisa ser feita em um desktop com ambiente gráfico.

## 3. Arquivos

| Arquivo | Responsabilidade |
|---|---|
| `main.py` | Interface Tkinter; cadastros, montagem, prévia, confirmação, histórico e CSV. |
| `modelos.py` | Produto, Item e Pedido; quantidade, subtotais, total e estado da montagem. |
| `pagamento.py` | Validação decimal, conversão para centavos e cálculo por forma de pagamento. |
| `repositorio.py` | Persistência SQLite, IDs, chaves estrangeiras e transação de venda/itens. |
| `controller.py` | Coordena cadastros e só finaliza o pedido depois da persistência bem-sucedida. |
| `memoria.py` | Repositório em memória para testar o contrato de cadastro. |
| `arquivos.py` | Leitura, validação e gravação segura de catálogo JSON. |
| `relatorios.py` | Exportação CSV a partir de comprovante confirmado. |
| `perfis.py` | Sessão fictícia e consulta de perfil. |
| `verificar.py` | Suíte automatizada de regressão A14–A18; não abre a GUI. |
| `ensaio-a18-logic.py` | Ensaio independente de quantidade inválida, correção e caso vizinho. |
| `comparar_ctk.py` | Comparação visual opcional; não é necessária para executar a aplicação. |
| `registro-a18.md` | Identificação, matriz, resultados, pendências e continuidade para A19. |
| `registro-a17.md` | Registro da versão-base preservado para rastreabilidade da candidata. |

## 4. Preparar e executar

Descompacte a pasta `aula18` e abra essa pasta no VS Code. No terminal integrado, confirme que o terminal está dentro da pasta que contém `main.py`.

O primeiro comando para conferir o ambiente é:

```bash
python --version
```

Depois execute a suíte antes de abrir a janela:

```bash
python -B verificar.py
```

Para executar o ensaio didático separado:

```bash
python -B ensaio-a18-logic.py
```

Para abrir a aplicação desktop:

```bash
python main.py
```

No Windows, se o comando `python` não estiver associado à instalação desejada, use `py` nos mesmos comandos (por exemplo, `py -B verificar.py`).

## 5. Banco de dados e isolamento dos ensaios

Por padrão, a aplicação usa:

```text
aula18/dados/sorveteria.db
```

O banco é criado quando a aplicação inicia. Ele não está incluído no ZIP, para que a primeira execução crie um arquivo local novo. Não use dados pessoais ou reais nos ensaios.

Para executar a janela com um banco separado, configure a variável `SORVETERIA_DB` **antes** de abrir a aplicação. Recomenda-se informar um caminho absoluto:

**PowerShell:**

```powershell
$env:SORVETERIA_DB = "$PWD\dados-ensaio\sorveteria-a18.db"
python main.py
```

**Prompt de Comando (cmd):**

```bat
set SORVETERIA_DB=%CD%\dados-ensaio\sorveteria-a18.db
python main.py
```

**Linux/macOS:**

```bash
SORVETERIA_DB="$PWD/dados-ensaio/sorveteria-a18.db" python main.py
```

A variável só altera o caminho usado pela aplicação; ela não copia nem apaga outro banco. A suíte `verificar.py` usa `TemporaryDirectory` e remove seus bancos de teste ao terminar. O teste de reabertura aponta para o mesmo arquivo temporário durante aquele caso.

## 6. Verificações e resultados

Comando automatizado:

```bash
python -B verificar.py
```

Resultado desta entrega: **todos os casos automatizados A14, A15, A16, A17 e A18 passaram**. A matriz em `registro-a18.md` identifica o que foi executado por código e o que ainda depende de inspeção manual.

Para reproduzir em outra pasta, copie ou descompacte novamente a pasta `aula18` em outro local, abra um terminal nessa cópia e execute, nesta ordem:

```bash
python --version
python -B verificar.py
python -B ensaio-a18-logic.py
```

Em seguida, em um desktop com Tkinter, execute `python main.py`. O teste automatizado não substitui a inspeção visual e de teclado.

## 7. Como conferir o fluxo corrigido

1. Cadastre um cliente e um produto fictícios, se o banco estiver vazio.
2. Na aba **Nova venda**, selecione um produto e adicione quantidade `2`.
3. Selecione o item na montagem, informe `0` no campo Quantidade e clique **Atualizar qtd.**.
4. A aplicação deve mostrar uma mensagem de erro e manter item, quantidade `2` e subtotal anteriores.
5. Informe `1` e clique **Atualizar qtd.** novamente. O item deve permanecer na montagem com subtotal recalculado.
6. Remova o item e confira o pedido vazio; depois adicione novamente se quiser continuar o fluxo.
7. Abra a prévia, confirme a venda e confira o histórico. Só depois da confirmação a venda e seus itens devem existir no banco.
8. Exporte o CSV e compare os campos com o comprovante da venda confirmada.

Se a quantidade for recusada, corrija o texto no campo e tente novamente. O erro não deve apagar o carrinho. Se o banco estiver em um caminho inesperado, feche a aplicação e confira `SORVETERIA_DB` e o caminho padrão descrito acima antes de reiniciar.

## 8. Limites conhecidos

- A execução automatizada e os ensaios em cópia foram realizados; a janela não foi validada visualmente neste ambiente.
- Tab/Shift+Tab, foco visível, acionamento por Enter/Espaço, mensagens e redimensionamento precisam ser conferidos manualmente no desktop.
- A validação por um colega sem explicação oral ainda precisa ser realizada e registrada.
- `customtkinter` é opcional; a ausência dele não impede a aplicação principal.

Não considere esses itens manuais concluídos até executá-los. A pasta e o comando desta candidata estão identificados no registro para que a mesma versão seja retomada na A19.
