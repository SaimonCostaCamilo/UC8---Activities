# Registro A13 — Exportação de comprovantes, perfis e integração de módulos

**Nome:** Saimon Camilo  
**Turma:** TDS  
**Data:** 13/11/2026

## Objetivo e conceitos
Exportar CSV a partir de comprovante confirmado, preservar o relatório diante de cancelamento/falha e separar sessão de usuário do estado da venda.

## Testes automatizados do núcleo
Comando: `python -B verificar.py`  
**Resultado:** aprovado nesta revisão. Os casos T00–T12 passaram, incluindo detecção de `assert` falso, ausência de exportação sem comprovante, CSV com acentos/aspas/delimitadores, leitura de volta, cabeçalho, quantidades e centavos, retrato confirmado independente da tela, cancelamento, falha de escrita, sessão/perfis, remoção do último item e regressões de JSON/pagamento.

## Testes automatizados da interface
Comando: `xvfb-run -a python -B verificar_interface.py`  
**Resultado:** aprovado nesta revisão em ambiente gráfico virtual (Tkinter/Tk 8.6). Foram executados: inicialização das telas; navegação com `Tab` e `Shift+Tab`; acionamento do botão Adicionar pela barra de espaço; tratamento de quantidade inválida seguido de correção; redimensionamento da janela com preservação dos widgets; perfis Caixa/Administração e permissão; seleção/remoção; tentativa de exportar sem comprovante; cancelamento do seletor; exportação e leitura do CSV; preservação do comprovante/arquivo após sair; inicialização e exportação nos catálogos de Pizzaria e Sorveteria.

## Checklist da interface
- **Controles e rótulos:** verificados pela criação dos widgets e pelos fluxos de integração automatizados.
- **Tab/Shift+Tab:** avanço e retorno de foco verificados por eventos de teclado.
- **Acionamento:** botão Adicionar acionado por evento de barra de espaço com foco.
- **Mensagem após erro e correção:** quantidade inválida acionou o tratamento de erro; após corrigir para `1`, a inclusão foi concluída.
- **Redimensionamento:** janela redimensionada de 980×700 para 1100×760; widgets principais permaneceram existentes.
- **Inspeção visual presencial:** não declarada como realizada. O teste em display virtual valida integração e geometria, mas não substitui a observação da aparência em um desktop real.

## Evidências e limites
Os testes usam dados fictícios e diretório temporário, sem alterar dados pessoais ou arquivos de venda reais. A execução gráfica foi feita com Xvfb porque o ambiente não oferece monitor físico. Antes de uma apresentação presencial, abra `main.py`, `pizzaria_main.py` e `sorveteria_main.py` no computador utilizado e confira a aparência final.

## Explicação individual
**Decisão técnica demonstrada:** o CSV recebe somente o comprovante confirmado; não consulta os campos atuais da interface. A escrita usa arquivo temporário e substituição após concluir a gravação, reduzindo o risco de destruir o destino anterior em uma falha.

**Conceito de perfis:** identificação informa o nome declarado; autenticação comprova identidade; autorização decide quais operações são permitidas. Esta atividade simula nome e perfil, portanto não realiza autenticação real.

**Reflexão pessoal para apresentação:** explique com suas próprias palavras uma dificuldade encontrada e como os testes ajudaram a localizar/corrigir o problema. Não foi inventada uma experiência pessoal neste registro.
