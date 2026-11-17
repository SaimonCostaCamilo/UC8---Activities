# A19 — Academia e demonstrações individuais

## Objetivo
Demonstrar uma aplicação desktop organizada por responsabilidades, reconhecer entidades e IDs, apresentar fluxo válido/erro/persistência e executar backup SQLite seguro. A candidata da sorveteria A18 continua preservada em `referencia-a18/` para a demonstração individual e comparação com o projeto integrador.

## Aplicação gráfica da academia
A entrega inclui uma aplicação executável em `main.py`, com abas **Alunos**, **Planos**, **Matrículas** e **Backup SQLite**. A interface está em `academia_ui.py`; persistência em `repositorio_academia.py`; cópia segura em `backup_sqlite.py`. O banco fictício/local é criado em `dados/academia-a19.db` na primeira execução.

```bash
python --version
python -B verificar.py
# teste da construção da janela (Linux com Xvfb):
xvfb-run -a python -B verificar_interface.py
python -B main.py
```

Na janela, cadastre aluno e plano, anote os IDs, crie matrícula usando esses IDs e confira a listagem. Na aba Backup SQLite, escolha um destino ainda inexistente. O programa não sobrescreve cópias existentes e verifica `PRAGMA integrity_check`.

## Candidata A18 preservada
`referencia-a18/` mantém o projeto desktop da sorveteria para retomada/revalidação do projeto integrador. Execute:

```bash
cd referencia-a18
python -B verificar.py
python -B ensaio-a18-logic.py
python main.py
```

Use banco fictício isolado conforme `referencia-a18/README-A18.md`.

## Arquivos
- `main.py`: ponto de entrada da janela da academia.
- `academia_ui.py`: interface Tkinter/ttk reutilizada pela A20.
- `repositorio_academia.py`: persistência SQLite da A19.
- `backup_sqlite.py`: backup via `Connection.backup()`, origem existente e destino novo.
- `verificar.py`: testes de backup e persistência em diretórios temporários.
- `verificar_interface.py`: smoke test da janela, cadastros, foco inicial e redimensionamento (não substitui inspeção manual de Tab/Shift+Tab).
- `academia_amostra.py`: amostra didática de entidades e IDs.
- `roteiro-demo.md` e `registro-a19.md`: apresentação e evidências.

## Limites
Testes automatizados não substituem apresentação individual, feedback real, inspeção presencial de foco/teclado/redimensionamento nem confirmação de envio. Registre somente o que executar e observar. A interface deve ser percorrida com Tab/Shift+Tab e acionada por teclado.
