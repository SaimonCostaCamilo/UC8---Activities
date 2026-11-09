# Registro A13 — CSV de vendas e simulação de perfis

**Nome:** Saimon Costa Camilo  
**Turma:** TDS  
**Data:** 09/11/2026  
**Pasta da atividade:** `aula13`

> **Nota de honestidade do registro:** as hipóteses da retomada abaixo foram preenchidas retrospectivamente a partir dos contratos e dos testes concluídos. Elas não devem ser apresentadas como anotações feitas antes de abrir o código. A versão A12 original não foi incluída no material recebido para esta revisão; por isso, a preservação física da cópia anterior precisa ser conferida no computador do aluno.

## Retomada sem consulta — hipóteses e comparação posterior

1. **Na A12, arquivo ausente e arquivo JSON inválido representam a mesma situação?**
   - Hipótese: não. Um arquivo ausente pode representar a primeira execução e, conforme o contrato do catálogo, resultar em uma lista vazia sem criar arquivo. Um JSON inválido existe, mas seu conteúdo não pode ser interpretado; deve gerar erro e não ser tratado silenciosamente como catálogo vazio.
   - Comparação após os testes: confirmado em `verificar.py` (T11). O caminho ausente retorna `[]`; JSON malformado e codificação inválida são rejeitados, sem alterar os bytes existentes.

2. **Por que um JSON que decodifica ainda precisa de validação de estrutura?**
   - Hipótese: porque a decodificação confirma apenas que o texto é JSON válido. Ela não garante que o conteúdo tenha o formato esperado pelo programa, nem que os campos, identificadores, nomes e preços sejam válidos.
   - Comparação após os testes: confirmado em T11. Catálogos com IDs repetidos, ID inválido, nome vazio ou preço não positivo são rejeitados pela validação do domínio.

3. **Na A09, como remover o último item do carrinho sem criar erro de seleção?**
   - Hipótese: verificar se existe uma seleção na Treeview, obter o identificador estável do item selecionado e removê-lo pelo código; depois atualizar a listagem. Não se deve presumir que sempre existe uma linha selecionada nem usar o índice visual como identidade.
   - Comparação após os testes: confirmado no teste de integração Tkinter. A seleção usa o IID/código; remover o último item deixa a lista vazia sem acessar uma seleção antiga.

4. **Qual informação da A09 permanece estável quando a ordem visual muda?**
   - Hipótese: o código/ID do produto. A posição ou índice da linha pode mudar quando a lista é reorganizada.
   - Comparação após os testes: confirmado pelo teste T09 e pelo uso do código como chave de `Pedido._itens` e IID da Treeview.

## Arquitetura antes do código

- `modelos.py`: mantém `Produto`, `Item`, `Pedido`, `Pizza`, `Bebida`, validação de quantidade, estados e comprovante. `Pedido.novo()` reinicia a montagem sem alterar uma cópia de comprovante já guardada pela interface.
- `pagamento.py`: mantém conversão monetária e cálculo com `Decimal`, evitando cálculos financeiros com ponto flutuante binário.
- `arquivos.py`: mantém validação, leitura e gravação segura do catálogo JSON.
- `relatorios.py`: recebe um comprovante confirmado, valida a estrutura, converte-o em linhas CSV, grava em arquivo temporário e substitui o destino somente após a escrita completa. Também oferece leitura de volta com `csv.DictReader`.
- `perfis.py`: mantém nome e perfil fictícios em uma sessão local; não autentica pessoas reais.
- `main.py`: integra montagem, seleção, prévia, confirmação, sessão demonstrativa e exportação CSV.
- `pizzaria_main.py`: configura a interface principal com produtos `Pizza` e `Bebida`.
- `sorveteria_main.py`: configura a mesma interface com produtos da sorveteria, incluindo `Picolé; edição verão`.
- `verificar.py`: executa testes de domínio, CSV, perfis e regressões sem GUI.
- `verificar_interface.py`: executa testes de integração Tkinter, incluindo seleção, perfis, cancelamento e exportação em ambiente com display.

**Dependências:** módulos padrão do Python e Tkinter/ttk. Não há instalação automática nem biblioteca externa obrigatória.

**Duração dos dados:** montagem e sessão ficam em memória; o comprovante confirmado é uma cópia independente; o arquivo CSV só é criado quando a ação de exportação recebe um caminho válido. Os testes usam diretórios temporários e dados fictícios.

## Matriz de execução

| Caso | Previsão | Observado | Correção/reteste ou situação |
|---|---|---|---|
| T00 — assert falso e restauração | A previsão falsa deve produzir `AssertionError`; depois a previsão correta deve passar. | Executado em `verificar.py`; a falha controlada foi detectada e a previsão correta passou. | Sem pendência técnica. |
| T01 — sem comprovante | Não exportar venda fictícia nem criar arquivo. | `exportar_csv(None, destino)` rejeitou a chamada; teste de interface também confirmou que a ação sem comprovante apresenta aviso e não abre gravação. | Sem pendência técnica. |
| T02 — CSV com caracteres especiais | Acentos, ponto e vírgula e aspas devem sobreviver à leitura de volta. | `Picolé; edição "verão"` e `Açaí com morango` foram lidos corretamente por `DictReader`. | Sem pendência técnica. |
| T03 — quantidade, centavos e total | Quantidade, preço e subtotal devem respeitar o cabeçalho; centavos permanecem inteiros e total tem duas casas. | 2 × 650 + 450 = 1.750 centavos; pagamento PIX de 87% = R$ 15,23. Cabeçalho e valores conferidos. | Sem pendência técnica. |
| T04 — retrato confirmado | Alterar campos ou iniciar nova montagem não deve modificar o comprovante exportável. | Exportação posterior à alteração do nome e início de outro pedido manteve o nome, subtotal e total originais. | Sem pendência técnica. |
| T05 — cancelamento do seletor | Cancelar não grava nem altera pedido, comprovante ou destino anterior. | Teste de integração substituiu o seletor por retorno vazio; comprovante e estado finalizado permaneceram iguais. | Sem pendência técnica. |
| T06 — falha de escrita | Não anunciar sucesso nem substituir o destino anterior; remover temporário. | Falha simulada de `os.replace` e pasta inexistente preservaram o arquivo anterior; temporário foi removido. | Sem pendência técnica. |
| T06b — inválido depois de válido | Uma exportação inválida posterior não pode substituir o CSV válido. | Subtotal inconsistente foi rejeitado e os bytes do CSV válido permaneceram iguais. | Sem pendência técnica. |
| T07 — perfil Caixa/Administração | Caixa não configura; Administração pode; sair limpa a sessão. | Testes de domínio e integração confirmaram os estados do menu e `pode_configurar()`. | Sem pendência técnica. |
| T08 — sair | Sair limpa somente a sessão fictícia; não apaga vendas ou relatórios. | Após sair, nome/perfil foram limpos e o CSV manteve os mesmos bytes. | Sem pendência técnica. |
| T09 — identidade e remoção do último item | O código identifica o item independentemente da posição visual; remover o último não deve gerar erro de seleção. | Teste de modelo e teste Tkinter selecionaram pelo IID/código e removeram o último item; lista e total ficaram vazios/zero. | Sem pendência técnica. |
| T10 — confirmação e estado | Cancelar preserva a montagem; prévia desatualizada é rejeitada; pedido finalizado bloqueia edição. | Todos os casos passaram no teste de domínio. | Sem pendência técnica. |
| T11 — regressão JSON A12 | Ausente, válido, malformado, codificação inválida e estrutura inválida devem ter tratamentos distintos. | Todos os casos passaram; falha de substituição preservou o catálogo anterior. | Sem pendência técnica. |
| T12 — regressão pagamento A12 | Decimal, conversão em centavos, fatores e entradas inválidas devem continuar funcionando. | Valores brasileiros, PIX, valor negativo e forma desconhecida foram verificados. | Sem pendência técnica. |
| GUI-01 — inicialização e perfis | As janelas devem ser construídas; Caixa e Administração devem apresentar permissões distintas. | Instâncias Mercado, Pizzaria e Sorveteria inicializadas sob display virtual; menu e autorização foram conferidos por teste. | Teste automatizado de integração concluído. |
| GUI-02 — exportação pela interface | Cancelamento não deve ter efeito; caminho escolhido deve gerar CSV legível. | Cancelamento preservou comprovante; exportação real em diretório temporário foi lida novamente. | Teste automatizado de integração concluído. |
| GUI-03 — transferência Pizzaria/Sorveteria | Os dois catálogos devem usar o mesmo contrato de exportação. | Uma venda fictícia de cada catálogo foi confirmada, exportada e lida de volta. | Teste automatizado de integração concluído. |

### Evidência numérica do CSV

Venda fictícia usada nos testes de `verificar.py`:

| Produto | Quantidade | Preço unitário | Subtotal |
|---|---:|---:|---:|
| Picolé; edição "verão" | 2 | 650 centavos | 1.300 centavos |
| Açaí com morango | 1 | 450 centavos | 450 centavos |
| **Total dos itens** | | | **1.750 centavos (R$ 17,50)** |

Forma de pagamento: PIX. Fator aplicado: 0,87. Total final: **R$ 15,23**. No CSV, os preços e subtotais por item são inteiros em centavos; `total_pedido_reais` registra o total final em reais com duas casas decimais e vírgula decimal.

## Explicação individual da decisão de implementação

**Decisão:** o exportador recebe o comprovante retornado por `Pedido.finalizar()` e não lê os widgets atuais. A interface guarda `copy.deepcopy(comprovante)` em `comprovante_exportacao`.

**Motivo:** o relatório precisa representar uma venda confirmada em um instante específico. Se o exportador consultasse os campos atuais, uma nova montagem ou alteração na tela poderia misturar dados de outra venda no comprovante anterior.

**Tratamento de erro:** o CSV é escrito em temporário no mesmo diretório. Somente depois de concluir a escrita e o `fsync`, `os.replace` substitui o destino. Se a operação falhar, o temporário é removido e o arquivo anterior é preservado. A interface só apresenta sucesso depois que `exportar_csv` retorna sem erro.

## Identificação, autenticação e autorização

- **Identificação demonstrativa:** o participante informa um nome fictício.
- **Escolha de perfil:** seleciona Caixa ou Administração.
- **Autenticação real:** não é implementada; não há senha, validação de identidade ou conta real.
- **Autorização demonstrativa:** `pode_configurar()` retorna verdadeiro somente para sessão ativa com perfil Administração.
- **Verificação na operação:** `abrir_configuracoes()` consulta novamente a permissão; esconder ou desabilitar o menu não é tratado como proteção suficiente.
- **Encerramento:** `sair()` limpa nome e perfil, mas não apaga pedido, comprovante ou relatório.

Em um sistema real, a identidade teria de ser autenticada e a permissão verificada na camada que executa a operação, não apenas na interface.

## Dificuldade, correção e nova tentativa

**Dificuldade técnica identificada:** impedir que uma exportação incompleta ou uma nova montagem alterasse o comprovante confirmado ou um CSV já existente.

**Correção aplicada:** manter uma cópia profunda do comprovante e gravar o CSV em arquivo temporário no mesmo diretório, substituindo o destino apenas depois da escrita completa.

**Nova tentativa:** foram executados os casos de alteração após confirmação, nova montagem, caminho vazio, destino inexistente, falha simulada de substituição e comprovante inconsistente depois de uma exportação válida. Os testes confirmaram a preservação do retrato e do arquivo anterior.

**Próximo teste recomendado no computador do aluno:** abrir as janelas sem display virtual, conferir visualmente os rótulos e os diálogos do sistema operacional e demonstrar ao professor o fluxo completo com os cliques. O teste automatizado confirma a lógica e os callbacks, mas não substitui a apresentação presencial.

## Arquivos, comandos e evidências

Todos os módulos da A13 estão na mesma pasta. Com Python e Tkinter disponíveis:

```bash
python verificar.py
python verificar_interface.py
python main.py
python pizzaria_main.py
python sorveteria_main.py
```

- `verificar.py`: testes de domínio e regressão sem GUI.
- `verificar_interface.py`: testes de integração Tkinter; em Linux sem display, pode ser executado com `xvfb-run -a python verificar_interface.py` se o Xvfb estiver instalado.
- `main.py`: interface principal.
- `pizzaria_main.py`: catálogo da Pizzaria.
- `sorveteria_main.py`: catálogo da Sorveteria, incluindo o nome com ponto e vírgula.
- Os arquivos gerados pelos testes ficam em diretórios temporários e são removidos ao final.

**Versão A12 anterior:** a cópia original não veio no ZIP disponibilizado para esta atualização. Ela deve permanecer preservada na pasta anterior do aluno; não foi reconstruída nem substituída por uma cópia inventada. A entrega atual contém a pasta A13 separada.

**Entrega:** conferir no computador o ZIP final, os arquivos Python e este registro antes de enviar pelo fluxo combinado com o professor.

## Conclusão

Os testes automatizados de domínio e de integração Tkinter foram executados com dados fictícios. O CSV foi exportado e lido de volta; os casos de ausência de comprovante, caracteres especiais, centavos, retrato confirmado, cancelamento, falha de escrita, perfis, encerramento de sessão, remoção do último item e transferência para Pizzaria/Sorveteria foram verificados.

A única providência externa que este pacote não consegue realizar é anexar a versão original da A12, pois ela não foi fornecida junto ao ZIP da A13. A apresentação visual ao professor também deve ser feita no computador do aluno, embora os callbacks e fluxos tenham sido exercitados em teste Tkinter automatizado.
