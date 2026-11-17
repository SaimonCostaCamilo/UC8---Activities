# A20 — Vínculos, recuperação e entrega final

**Base:** pacote A19 fornecido, preservado em `../A19/`.  
**Candidata desktop:** `../A19/referencia-a18/` (cópia sem alterações).  
**Dados:** somente fictícios; os testes SQLite criam banco temporário e o removem ao terminar.

## Conteúdo desta pasta

- `vinculos.py` — valida IDs de alunos, planos e matrículas; recusa referências órfãs e indica bloqueio de exclusão vinculada.
- `relacoes_sqlite.py` — demonstra `PRAGMA foreign_keys=ON`, chaves estrangeiras e `ON DELETE RESTRICT`.
- `verificar.py` — asserts para vínculos válidos, referências ausentes, IDs inválidos/duplicados, exclusão vinculada, preservação após erro e execução dos módulos.
- `ensaio-a20-logic.py` — exemplo mínimo pedido na teoria.
- `ensaio-a20-window.py` — roteiro de registro; complete após executar a aplicação.
- `registro-a20.md` — matriz T01–T10 e reflexão individual.
- `entrega-final.md` — inventário, evidências e conferência em pasta limpa.
- `roteiro-revalidacao-a19.md` — pendência selecionada a partir do registro A19.

## Preparar e executar no VS Code

Abra esta pasta `A20` no VS Code e use o terminal integrado:

```bash
python --version
python -B ensaio-a20-logic.py
python -B vinculos.py
python -B relacoes_sqlite.py
python -B verificar.py
```

Resultado esperado do ensaio mínimo:
```text
True
True
False
```

O verificador imprime os casos aprovados. Ele não substitui a inspeção manual da aplicação desktop.

## Regras do exercício

1. Matrícula liga aluno e plano por `aluno_id` e `plano_id`, nunca pelo nome.
2. IDs devem ser inteiros positivos; `bool` não é aceito como inteiro válido.
3. IDs repetidos e referências inexistentes são recusados antes de aceitar os dados.
4. `pode_excluir_aluno` apenas informa se existe matrícula vinculada; não apaga registros.
5. Em SQLite, `PRAGMA foreign_keys=ON` deve ser executado em cada conexão.
6. `ON DELETE RESTRICT` impede apagar aluno/plano referenciado. O erro deve ser tratado com rollback, preservando os dados.

## Candidata desktop e pendência da A19

A versão desktop permanece em `../A19/referencia-a18/`; ela não foi reescrita nem substituída pelos scripts didáticos. Leia `README-A18.md`. Para executar a candidata:

```bash
cd ../A19/referencia-a18
python -B verificar.py
python -B ensaio-a18-logic.py
python main.py
```

Para isolar a aplicação com banco fictício, configure `SORVETERIA_DB` conforme o README-A18. Não use banco pessoal/real.

A pendência selecionada no registro A19 foi a inspeção manual da GUI e navegação por teclado. Os testes desta pasta não provam essa inspeção. Execute a aplicação em desktop e registre, em `roteiro-revalidacao-a19.md` e `registro-a20.md`, o fluxo válido, recusa/correção, Tab/Shift+Tab, foco, mensagens e redimensionamento. Se não executar, mantenha como pendente.

## Conferência em pasta limpa

1. Extraia uma cópia nova do ZIP em outro diretório.
2. Abra a pasta `A20` no VS Code.
3. Rode os quatro comandos acima.
4. Abra a candidata desktop em `A19/referencia-a18` e siga seu README.
5. Anote os comandos, caminhos e resultados realmente observados em `entrega-final.md`.
6. Preserve a versão anterior e uma cópia local do ZIP entregue.

## Limites conhecidos

- Os dados SQLite de `relacoes_sqlite.py` são temporários; não são o banco da aplicação desktop.
- A amostra `A19/academia_amostra.py` é JSON fictício e não comprova GUI nem banco relacional.
- Os scripts de A20 demonstram a regra de vínculo separadamente; não alteram automaticamente a candidata desktop.
- A inspeção visual/teclado da GUI e feedback de outra pessoa dependem de execução humana no desktop.
- Não declare feedback, envio, recebimento, teste manual ou evidência que não tenha observado.
