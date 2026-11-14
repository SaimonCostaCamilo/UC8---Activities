# A17 — Sorveteria integrada e comparação visual

## Objetivo
Integrar cadastros e vendas em SQLite, mantendo a montagem do pedido em memória até a confirmação. A venda e todos os itens são gravados em uma única transação; qualquer falha desfaz o conjunto.

## Organização
- `modelos.py`: Produto, Item e Pedido; a montagem e sua prévia permanecem em memória.
- `pagamento.py`: interpretação decimal e cálculo por forma de pagamento.
- `repositorio.py`: SQLite, chaves estrangeiras, cadastros, histórico e gravação atômica de venda/itens.
- `controller.py`: coordena cadastro e finalização; só cria o comprovante depois da gravação bem-sucedida.
- `main.py`: interface Tkinter com catálogo, clientes, montagem, prévia, confirmação, histórico e CSV.
- `relatorios.py`: exportação CSV a partir do comprovante confirmado.
- `arquivos.py`: leitura/escrita segura de catálogo JSON, mantida como módulo de apoio.
- `perfis.py`: simulação local de sessão; não autentica usuários reais.
- `memoria.py`: repositório em memória para testes de cadastro; não persiste vendas.
- `comparar_ctk.py`: comparação opcional de foco/teclado; CustomTkinter não é dependência do núcleo.
- `verificar.py`: testes automatizados sem abrir janela.
- `registro-a17.md` e `relatorios.md`: registro e relatório da atividade.

## Execução
Requer Python 3.10+ e Tkinter. Execute no terminal, dentro desta pasta:

```bash
python --version
python -B verificar.py
python main.py
```

Opcionalmente, instale `customtkinter` para comparar a janela alternativa:

```bash
python -m pip install customtkinter
python comparar_ctk.py
```

## Regras de negócio
1. Produtos e clientes são identificados por IDs do banco.
2. A venda exige cliente selecionado, itens válidos e forma de pagamento conhecida.
3. Antes de inserir, o repositório confere se cada produto ainda existe e se nome/preço correspondem ao retrato da montagem.
4. O cabeçalho da venda e todos os itens usam a mesma conexão e transação `BEGIN IMMEDIATE`; o commit ocorre somente após todos os itens. Erros provocam rollback.
5. O controller só chama `Pedido.finalizar` depois do retorno bem-sucedido do repositório. Em falha, o pedido continua em montagem.
6. Chaves estrangeiras bloqueiam exclusão de clientes/produtos vinculados. O histórico guarda também nome e preço unitário do momento da venda.
7. O CSV é gerado a partir do comprovante confirmado, não de widgets ou de uma montagem ainda aberta.

## Banco de dados
A aplicação cria `dados/sorveteria.db` ao iniciar. O banco não é versionado e deve conter apenas dados fictícios durante os testes.
