# Aula 13 — Relatórios CSV e simulação de perfis

## Objetivo

Exportar um retrato de venda confirmada para CSV e comparar, em uma simulação local, as ações disponíveis aos perfis Caixa e Administração.

O projeto utiliza dados fictícios. Não implementa autenticação real e não possui valor fiscal.

## Arquivos

| Arquivo | Responsabilidade |
|---|---|
| `main.py` | Continuação da aplicação Mercado da A12, com pedido, comprovante CSV e perfis. |
| `pizzaria_main.py` | Demonstra a aplicação da Pizzaria usando o mesmo contrato de exportação. |
| `sorveteria_main.py` | Recebe o mesmo contrato de exportação; inclui o produto “Picolé; edição verão”. |
| `modelos.py` | Pedido, produtos, itens, estados e comprovante. Reutilizado da A12; inclui `novo()` para reiniciar uma montagem. |
| `pagamento.py` | Conversão monetária e cálculo com `Decimal`, reutilizado da A12. |
| `arquivos.py` | Leitura, validação e gravação JSON, reutilizado da A12. |
| `relatorios.py` | Validação do comprovante, criação do CSV, gravação atômica e leitura de volta. |
| `perfis.py` | Sessão fictícia Caixa/Administração. |
| `verificar.py` | Testes sem GUI para CSV, perfis e regressões da A09/A12. |
| `verificar_interface.py` | Testes de integração Tkinter para perfis, seleção, cancelamento e exportação nos catálogos. |
| `registro-a13.md` | Registro acadêmico e matriz de execução. |

Todos os módulos Python ficam juntos na mesma pasta, para que os imports locais funcionem.

## Como executar

Abra a pasta `aula13` no VS Code. Use o terminal integrado:

```bash
python verificar.py
python verificar_interface.py
```

Para abrir a continuação do seu sistema de Mercado:

```bash
python main.py
```

Para abrir a demonstração da Pizzaria:

```bash
python pizzaria_main.py
```

Para abrir a demonstração da Sorveteria:

```bash
python sorveteria_main.py
```

É necessário ter Python com Tkinter disponível. Não há instalação automática nem dependências externas.

## Como funciona o comprovante

A exportação recebe somente o dicionário de comprovante devolvido por `Pedido.finalizar`. Ela não consulta `Entry`, `Treeview` ou outros widgets.

A aplicação guarda uma cópia independente do comprovante confirmado em memória. Assim, alterar campos ou iniciar uma nova montagem não modifica o retrato selecionado para exportação. O arquivo só é criado quando o usuário escolhe explicitamente **Exportar comprovante CSV** e confirma um caminho no seletor.

Sem comprovante confirmado, não há exportação. Cancelar o seletor retorna sem gravar. Uma falha de escrita não deve anunciar sucesso nem substituir o arquivo anterior.

## Contrato CSV

O arquivo usa:

- Delimitador `;`.
- `csv.writer` e `csv.DictReader`.
- `newline=""`.
- Codificação `UTF-8 com BOM` (`utf-8-sig`) para compatibilidade com leitores que esperam a marca de codificação.
- Gravação em temporário no mesmo diretório e `os.replace` após a escrita completa.

Cabeçalho:

```text
id;nome;quantidade;preco_unitario_centavos;subtotal_centavos;forma_pagamento;total_pedido_reais
```

`preco_unitario_centavos` e `subtotal_centavos` são inteiros em centavos. `total_pedido_reais` é o total final da forma de pagamento, escrito com duas casas decimais e vírgula decimal, por exemplo `15,23`. Essa convenção também está no cabeçalho e neste README.

Os campos de texto podem conter acentos, ponto e vírgula ou aspas. Por isso, o CSV é escrito com `csv.writer`, que faz o escape necessário, e lido novamente com `csv.DictReader`.

Este CSV é um comprovante didático, não um documento fiscal.

## Simulação de perfis

A tela permite informar um nome fictício e escolher Caixa ou Administração.

- Caixa: `pode_configurar()` retorna `False`.
- Administração: `pode_configurar()` retorna `True`.
- Sair limpa nome e perfil da sessão demonstrativa.
- Sair não apaga comprovantes, vendas ou relatórios.

Nome e perfil escolhidos não provam identidade. Não há senha nem autenticação. Esconder/desabilitar um botão não protege um sistema real; por isso a operação de configuração também consulta `pode_configurar()`. Em produção, a autorização precisaria ser validada na camada que executa a operação.

## Decisões de implementação

1. O relatório parte do comprovante confirmado, não do conteúdo atual da tela.
2. O comprovante exportável é uma cópia profunda separada da montagem. `Pedido.novo()` pode limpar a montagem sem reescrever esse retrato.
3. Os preços e subtotais permanecem inteiros em centavos; somente o total final é formatado em reais com duas casas.
4. O arquivo temporário fica no mesmo diretório do destino para permitir substituição atômica.
5. O projeto conserva o catálogo JSON da A12 e o cálculo monetário anterior, em vez de reescrevê-los sem necessidade.
6. A chave estável do item é seu código/ID, não a posição visual da linha.

## Testes

Execute `python verificar.py`. Os testes usam arquivos temporários e dados fictícios. A matriz em `registro-a13.md` separa o que foi executado automaticamente do que ainda depende de observação visual no computador.

`verificar_interface.py` exercita os callbacks e os fluxos da interface em ambiente com display, incluindo cancelamento do seletor, perfis, seleção/remoção e exportação de vendas da Pizzaria e da Sorveteria. Em Linux sem display físico, pode ser executado com `xvfb-run -a python verificar_interface.py` se o Xvfb estiver instalado. A apresentação visual e a demonstração ao professor ainda devem ser feitas no computador do aluno.

A versão original da A12 deve ser mantida separadamente. Ela não foi incluída no ZIP recebido para esta atualização e, portanto, não foi reconstruída nem substituída.
