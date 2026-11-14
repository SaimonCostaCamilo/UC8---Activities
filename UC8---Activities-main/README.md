# UC8 — Atividades de Python (A01–A18)

**Aluno:** Saimon Camilo  
**Turma:** TDS  
**Data de atualização:** 13/11/2026

Entrega organizada em 18 pastas, uma por atividade. Cada pasta `aulaNN` contém os arquivos de implementação, o README específico quando existente e um único registro consolidado `registro-aNN.md`. Os registros identificam objetivo, decisões, evidências e limites reais dos testes; não apresentam verificações manuais como concluídas quando não foram executadas.

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

## Estrutura

- `aula01/` a `aula18/`: implementações e registros individuais.
- `aulaNN/registro-aNN.md`: registro oficial de cada atividade.
- `aulaNN/README.md`: instruções específicas da atividade, quando fornecidas.
- A atividade 11 mantém os arquivos executáveis dentro de `aula11/Aula 11/`; seu registro consolidado fica em `aula11/registro-a11.md`.

## Requisitos e execução

- Python 3.10 ou superior (a validação desta revisão foi feita com Python 3.13.5).
- Tkinter para abrir as interfaces gráficas.
- Não há dependências externas obrigatórias para o núcleo das atividades; `comparar_ctk.py` é opcional e depende de CustomTkinter.
- Abra a pasta da atividade desejada no VS Code e consulte o README local.
- Para as atividades com verificador, execute-o a partir da própria pasta. Exemplo: `python -B verificar.py`.
- Para abrir uma interface, execute `python main.py` na pasta que contém esse arquivo. Na A11, entre primeiro em `aula11/Aula 11/`.

## Auditoria de testes desta entrega

A execução foi realizada novamente nesta revisão. Resultado: **15 verificadores/ensaios automatizados executados; os 15 passaram na execução final.** Na primeira tentativa, A07 falhou porque o assert exigia uma expressão textual mais específica que a mensagem real; o teste foi corrigido para conferir o trecho estável da mensagem e reexecutado com sucesso. Portanto, **todos os verificadores automatizados de núcleo disponíveis para as aulas A06–A18 passaram**, incluindo a cópia de A10 na subpasta `Aula 10` e A11 na subpasta `Aula 11`.

| Aula | Verificação | Resultado nesta revisão |
|---:|---|---|
| 01–05 | Registros e código; sem script automatizado próprio | Evidências/documentação revisadas; não declarar suíte automatizada |
| 06 | `python -B verificar_modelo.py` | Aprovado |
| 07 | `python -B verificar.py` | Aprovado após ajuste do assert da mensagem |
| 08–10 | `python -B verificar.py` | Aprovados |
| 11 | `python -B verificar.py` em `aula11/Aula 11/` | Aprovado (T01–T08) |
| 12 | `python -B verificar.py` | Aprovado (T01–T11) |
| 13 | `python -B verificar.py` | Aprovado (T00–T12) |
| 13 | `python -B verificar_interface.py` | Não executável neste ambiente: sem display gráfico (`TclError`) |
| 14–17 | `python -B verificar.py` | Aprovados, incluindo regressões acumuladas |
| 18 | `python -B verificar.py` e `python -B ensaio-a18-logic.py` | Aprovados |

Também foram compilados **102 arquivos Python**, sem erros de sintaxe. A suíte de verificações automatizadas não valida aparência, navegação por teclado, foco, redimensionamento nem operação visual em desktop. Esses itens continuam pendentes quando indicados nos registros.

## O que está validado e o que falta

**Validado:** verificadores automatizados existentes das A06–A18; regressões acumuladas A14–A18; ensaio lógico A18; compilação dos arquivos Python; organização dos 18 registros.

**Não confirmado por esta execução:** testes manuais de interface/teclado; execução visual das atividades A01–A05; verificação de interface A13 (ambiente sem display); comparação visual opcional ttk/CustomTkinter da A17; validação por colega. Não é correto afirmar que todos os testes possíveis foram validados.

## Observações de segurança e dados

Os dados de teste devem ser fictícios. As atividades com SQLite/JSON/CSV possuem seus próprios caminhos de dados; leia o README da aula antes de executar a interface. Na A18, `SORVETERIA_DB` permite apontar para um banco isolado.
