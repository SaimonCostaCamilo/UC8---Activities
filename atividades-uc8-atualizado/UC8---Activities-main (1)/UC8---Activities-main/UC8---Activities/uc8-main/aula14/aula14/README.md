# UC8 — Aula 14: Produtos persistidos com SQLite

Esta pasta contém somente os arquivos da A14. O projeto foi implementado a partir dos módulos de apoio já utilizados na A13, preservando os contratos de modelo, pagamento decimal, JSON, CSV e sessão demonstrativa.

## Arquivos

- `main.py` — interface Tkinter para cadastrar produtos, consultar a listagem persistida e adicioná-los a um pedido em memória.
- `repositorio.py` — repositório SQLite com criação idempotente das tabelas `produtos` e `clientes`, validações e SQL parametrizado.
- `modelos.py` — classes `Produto`, `Item` e `Pedido`; quantidades e totais continuam no modelo em memória.
- `pagamento.py` — interpretação monetária com `Decimal`, cálculo e conversão para centavos.
- `arquivos.py` — validação, leitura e gravação segura do catálogo JSON.
- `relatorios.py` — exportação CSV a partir de comprovante confirmado.
- `perfis.py` — simulação local de sessão/perfil; não é autenticação real.
- `verificar.py` — testes automatizados sem interface gráfica.
- `registro-a14.md` — matriz de testes, resultados automatizados, explicações e pendências de validação manual.

## Executar

Use Python 3.10 ou superior. Não há dependências externas; Tkinter deve estar disponível na instalação do Python.

1. Abra o terminal nesta pasta `A14`.
2. Execute os testes: `python verificar.py`.
3. Abra a interface: `python main.py`.

O banco será criado na primeira execução da interface em `dados/mercado.db`. O caminho é resolvido a partir da localização de `main.py`, não da pasta corrente do terminal. Não apague esse arquivo se quiser conservar os cadastros.

## Estrutura SQLite

Tabela `produtos`:

| id | nome | preco_centavos |
|---:|---|---:|
| 1 | Arroz | 750 |

Tabela `clientes`:

| id | nome |
|---:|---|
| 1 | Cliente de teste |

Os valores são enviados separadamente da instrução SQL, por exemplo `con.execute(sql, (nome, preco_centavos))`. A gravação recebe `commit()` antes de a interface limpar os campos ou atualizar a listagem. Em caso de erro, a exceção é propagada e os campos permanecem disponíveis para correção.

## Limite desta etapa

Produtos e clientes são persistidos no SQLite. O pedido/carrinho continua intencionalmente em memória nesta aula; persistência de pedidos não foi adicionada. Os testes automatizados não substituem a conferência manual da janela, do percurso por Tab/Shift+Tab e do redimensionamento em um ambiente com interface gráfica.
