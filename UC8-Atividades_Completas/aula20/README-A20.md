# A20 — Relacionamentos, recuperação e encerramento

## Objetivo
Consolidar relacionamentos por ID, impedir referências órfãs, comparar validação em memória com integridade referencial SQLite, proteger exclusões vinculadas e revalidar aplicação desktop.

## Aplicação gráfica integrada
A A20 possui ponto de entrada próprio `main.py`. Ele reutiliza a interface Tkinter/ttk da A19, mas injeta `RepositorioRelacional`, que persiste em `dados/academia-a20.db` e aplica `PRAGMA foreign_keys=ON`, `FOREIGN KEY` e `ON DELETE RESTRICT`. A validação por IDs de `vinculos.py` também é aplicada antes da gravação. Assim, o cadastro de matrículas na janela utiliza o repositório relacional da A20; os exemplos não ficam apenas isolados.

```bash
python --version
python -B ensaio-a20-logic.py
python -B vinculos.py
python -B relacoes_sqlite.py
python -B verificar.py
# teste da construção da janela (Linux com Xvfb):
xvfb-run -a python -B verificar_interface.py
python -B main.py
```

Na janela, cadastre aluno e plano, crie matrícula com os IDs e confira a listagem. O repositório impede IDs inexistentes e bloqueia exclusão de aluno/plano com matrícula vinculada. Para repetir testes, use o banco temporário criado pelo verificador.

## Relação com A19 e projeto integrador
- `../aula19/main.py`: demonstração gráfica A19 e backup.
- `main.py`: janela A20 com o mesmo fluxo visual e persistência relacional reforçada.
- `../aula19/referencia-a18/`: candidata original da sorveteria, preservada para revalidação do projeto integrador.

A A20 não substitui nem altera os arquivos da candidata A18. Acrescenta módulo de demonstração de relacionamentos por ID, coerente com o tema de academia e matrícula dos anexos A19/A20.

## Arquivos
- `main.py`: janela A20 integrada.
- `repositorio_relacional.py`: repositório SQLite com FK e RESTRICT.
- `vinculos.py`: valida IDs positivos, únicos e referências existentes.
- `relacoes_sqlite.py`: demonstra FK, referência órfã, exclusão restrita e rollback.
- `verificar.py`: testes unitários e de integração do repositório.
- `verificar_interface.py`: smoke test da janela A20, fluxo integrado, recusa, foco inicial e redimensionamento (não substitui inspeção manual de Tab/Shift+Tab).
- `ensaio-a20-logic.py`: sequência didática mínima.
- `ensaio-a20-window.py`: roteiro de inspeção manual da janela.
- `roteiro-revalidacao-a19.md`: revalidação da candidata desktop A18.

## Critérios e limites
O verificador automatizado não afirma inspeção visual, apresentação individual ou feedback de colega/professor. Execute a janela em desktop real para verificar Tab/Shift+Tab, foco visível, Enter, mensagens, correção de erros e redimensionamento. Registre resultados observados no registro A20. Apresentação e envio ao canal do curso também dependem de você.
