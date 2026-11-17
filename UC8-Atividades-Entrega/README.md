# UC8 — Atividades de Python (A01–A20)

**Aluno:** Saimon Camilo  
**Turma:** TDS  
**Data de atualização:** 13/11/2026

Entrega organizada em 20 pastas, uma por atividade. Cada pasta `aulaNN` contém os arquivos de implementação, o README específico quando existente e um único registro consolidado `registro-aNN.md`. Os registros identificam objetivo, decisões, evidências e limites reais dos testes; não apresentam verificações manuais como concluídas quando não foram executadas.

## Índice das atividades

| Aula | Atividade | Conteúdo principal |
|---:|---|---|
| 01 | Fundamentos de entrada, saída e cadastro | Tipos, funções, condições e validação de entrada |
| 02 | Cadastro e controle de estado | Callbacks, leitura de campos, inclusão e listagem |
| 03 | Conversão de moedas | Cálculos, cotações fictícias e preservação do último resultado válido |
| 04 | Sistema escolar | Validação de identificação/notas e cálculo de média |
| 05 | Organização de interface escolar | Frames, consultas, janelas e estado confirmado |
| 06 | Modelagem de aluno | Classes, instâncias, métodos e validação de domínio |
| 07 | Modelos de domínio e testes | Produto, pedido, quantidade e subtotais |
| 08 | Carrinho e pagamento | Separação de modelo/pagamento e precisão monetária |
| 09 | Integração de pedido | Interface, seleção, carrinho e pagamento |
| 10 | Interface gráfica de pedidos | Validações e integração dos módulos |
| 11 | Pizzaria | Estados do pedido, prévia, cancelamento e confirmação |
| 12 | Mercado | Catálogo JSON, carrinho e pagamento |
| 13 | Comprovantes e perfis | Exportação CSV, sessão e preservação de arquivos |
| 14 | Persistência SQLite | Repositório, validação e reabertura do banco |
| 15 | CRUD de produtos | Edição/exclusão por ID e início de clientes |
| 16 | Controller e clientes | Contrato de repositório e CRUD completo |
| 17 | Sorveteria integrada | Transação de venda/itens, catálogo, histórico e CSV |
| 18 | Regressão e reprodução | Correções de quantidade/moeda, testes e README reproduzível |
| 19 | Academia e demonstrações individuais | Entidades, responsabilidades, backup SQLite seguro e demonstração individual |
| 20 | Relacionamentos, recuperação e encerramento | Vínculos por ID, referências órfãs, chaves estrangeiras, `ON DELETE RESTRICT` e revalidação |

## Estrutura

- `aula01/` a `aula20/`: implementações e registros individuais.
- `aulaNN/registro-aNN.md`: registro oficial de cada atividade.
- `aulaNN/README.md`: instruções específicas da atividade, quando fornecidas.
- A atividade 11 mantém os arquivos executáveis dentro de `aula11/Aula 11/`; seu registro consolidado fica em `aula11/registro-a11.md`.
- A A19 inclui a candidata desktop A18 em `aula19/referencia-a18/`, preservada para demonstração e revalidação na A20.
- A A20 mantém os ensaios de vínculo separados da aplicação desktop; não afirma integração automática com a candidata A18.

## Requisitos e execução

- Python 3.10 ou superior (a validação desta revisão foi feita com Python 3.13.5).
- Tkinter para abrir as interfaces gráficas.
- Não há dependências externas obrigatórias para o núcleo das atividades; `comparar_ctk.py` é opcional e depende de CustomTkinter.
- Abra a pasta da atividade desejada no VS Code e consulte o README local.
- Para as atividades com verificador, execute-o a partir da própria pasta. Exemplo: `python -B verificar.py`.
- Para abrir uma interface, execute `python main.py` na pasta que contém esse arquivo. Na A11, entre primeiro em `aula11/Aula 11/`.

## Auditoria de testes desta entrega

A revisão executou novamente os verificadores disponíveis. **16 scripts `verificar.py` passaram** nas atividades A07–A20, incluindo as duas cópias/variantes da A10 e a cópia de referência da A18 na A19. Também passaram os verificadores complementares `aula06/verificar_modelo.py` e `aula18/ensaio-a18-logic.py`. O teste gráfico `aula13/verificar_interface.py` passou com `xvfb-run -a`, incluindo navegação por teclado, acionamento por barra de espaço, recuperação após erro e redimensionamento. Ao todo, foram 18 verificações de núcleo/complementares, além da integração gráfica da A13. As atividades A01–A05 não possuem verificador automatizado próprio.

| Aula | Verificação | Resultado nesta revisão |
|---:|---|---|
| 01–05 | Revisão de código e documentação | Sem verificador automatizado próprio; execução manual não declarada |
| 06 | `python -B verificar_modelo.py` | Aprovado |
| 07–09 | `python -B verificar.py` | Aprovados |
| 10 | `python -B verificar.py` na raiz e em `Aula 10/` | Ambos aprovados |
| 11 | `python -B verificar.py` em `aula11/Aula 11/` | Aprovado |
| 12 | `python -B verificar.py` | Aprovado |
| 13 | `python -B verificar.py` | Aprovado |
| 13 | `xvfb-run -a python -B verificar_interface.py` | Aprovado nesta revisão: Tab/Shift+Tab, barra de espaço, erro/correção, redimensionamento, perfis, CSV e fluxos de catálogo |
| 14–17 | `python -B verificar.py` | Aprovados, incluindo regressões acumuladas |
| 18 | `python -B verificar.py` e `python -B ensaio-a18-logic.py` | Aprovados; T07 testa explicitamente `True` e `False` |
| 19 | `python -B verificar.py` | Aprovado: backup SQLite, integridade, origem/destino e recusas |
| 20 | `python -B verificar.py` | Aprovado: IDs, referências, exclusão vinculada, rollback e reprodução |

Também foi feita compilação dos 124 arquivos Python da entrega, sem erros de sintaxe. A suíte automatizada não valida aparência, navegação por teclado, foco, redimensionamento nem operação visual em desktop. Esses itens permanecem pendentes quando indicados nos registros.

## O que está validado e o que falta

**Validado:** verificadores automatizados A06–A12 e A13–A20; teste gráfico automatizado da A13 em Xvfb, incluindo navegação por teclado, acionamento, correção de erro e redimensionamento; testes booleanos `True`/`False` da A18; backup e integridade SQLite da A19; vínculos por ID e integridade referencial da A20; compilação dos arquivos Python.

**Não confirmado por esta execução:** execução visual das atividades A01–A05; inspeção presencial da aparência em desktop real; apresentação individual e feedback de colega/professor; fluxo manual de backup por CLI com dados locais. Não é correto afirmar que todos os testes possíveis foram validados.

## Observações de segurança e dados

Os dados de teste devem ser fictícios. As atividades com SQLite/JSON/CSV possuem seus próprios caminhos de dados; leia o README da aula antes de executar a interface. Na A18, `SORVETERIA_DB` permite apontar para um banco isolado.
