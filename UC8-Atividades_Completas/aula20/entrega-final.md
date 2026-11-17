# Minha entrega final — A20

**Identificação:** Saimon Camilo · TDS · 13/11/2026

## Inventário técnico
- `aula19/main.py`: janela A19 de academia e backup SQLite.
- `aula20/main.py`: janela A20 de academia com repositório relacional integrado.
- `aula20/vinculos.py`: validação em memória por IDs.
- `aula20/relacoes_sqlite.py`: FK, RESTRICT, rollback e integridade.
- `aula20/verificar.py`: testes de integração em diretório temporário.
- `aula19/referencia-a18/`: candidata desktop do projeto integrador preservada.

## Evidências automatizadas
- A19: `python -B verificar.py` — backup seguro, origem/destino, integridade, persistência e proteção contra exclusão vinculada aprovados.
- A20: `python -B verificar.py` — IDs, referências órfãs, bool/negativos/duplicados, FK, RESTRICT, rollback e repositório integrado aprovados.
- Os dados de teste são fictícios e temporários; os bancos locais da interface são criados somente quando você executa `main.py`.

## Evidências que dependem do aluno
- Executar as janelas A19 e A20 em desktop e inspecionar Tab/Shift+Tab, foco, mensagens, Enter e redimensionamento.
- Reexecutar a candidata A18 seguindo `roteiro-revalidacao-a19.md`.
- Fazer a demonstração individual, responder à pergunta técnica e registrar feedback real.
- Conferir ZIP extraído, cópia local e recebimento no canal combinado.

**Não registrar como concluído antes de executar.** Complete os campos no `registro-a20.md` com data, comandos, caminhos e observações reais.
