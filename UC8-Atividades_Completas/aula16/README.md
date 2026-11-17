# A16 — Controller, repositórios e cadastro completo de clientes

## Objetivo
Separar a coordenação da interface (`controller.py`) do armazenamento (`repositorio.py` e `memoria.py`), mantendo o mesmo contrato para produtos e clientes. Produtos e clientes persistem no SQLite; o pedido continua somente em memória.

## Estrutura
- `main.py`: interface Tkinter; callbacks recebem os campos, chamam o controller e tratam falhas sem apagar a edição.
- `controller.py`: coordena listar, salvar (incluir/editar) e excluir sem importar Tkinter.
- `repositorio.py`: validações e implementação SQLite.
- `memoria.py`: implementação em memória com o mesmo formato de retorno.
- `modelos.py`, `pagamento.py`, `arquivos.py`, `relatorios.py`, `perfis.py`: módulos retomados das aulas anteriores.
- `verificar.py`: testes automatizados sem abrir a janela.
- `dados/mercado.db`: criado quando a aplicação inicia com SQLite; não versionar dados reais.

## Como executar
Requer Python 3.10+ e Tkinter.

```bash
python --version
python -B verificar.py
python main.py
```

Execute os comandos a partir desta pasta. `verificar.py` usa bancos e arquivos temporários e não altera o banco de uso da interface.

## Contrato de cadastro
- Produto: `{"id", "nome", "preco_centavos"}`.
- Cliente: `{"id", "nome"}`.
- `adicionar_*` devolve o registro criado; `listar_*` devolve uma lista de dicionários; `editar_*` e `excluir_*` devolvem booleano.
- Exclusão só acontece com `confirmado=True`; cancelamento retorna `False`.
- ID inexistente não é tratado como sucesso.
- Falhas de validação/SQLite são propagadas ao callback; os campos permanecem preenchidos.

## Persistência e estado
O SQLite guarda produtos e clientes após fechar/reabrir. `Pedido` continua em memória e não é gravado no banco.
