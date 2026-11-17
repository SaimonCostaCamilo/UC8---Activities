# A19 — Academia e demonstrações individuais

Pacote da segunda aula de encerramento da UC8. Contém a candidata A18 preservada em `referencia-a18/`, a amostra de academia, roteiro individual, registro da aula e um ensaio seguro de backup SQLite.

## O que foi preparado
- A candidata A18 foi copiada do ZIP `UC8---Activities-main (2).zip` sem editar seus arquivos.
- O README da candidata foi mantido em `referencia-a18/README-A18.md`.
- O script `backup_sqlite.py` exige origem existente e destino novo, usa `Connection.backup()`, consulta integridade e preserva destino existente.
- `verificar.py` cria bancos fictícios temporários e testa cópia, consulta conhecida, integridade, origem ausente, destino existente e caminhos iguais.
- `preparar_ensaio.py` cria uma base fictícia persistente somente se o arquivo ainda não existir.
- O registro separa evidência automatizada de apresentação/feedback ainda pendentes.

## Execução no VS Code

Abra a pasta `A19` no VS Code e use o terminal integrado.

1. Conferir a candidata A18:
```bash
cd referencia-a18
python -B verificar.py
python -B ensaio-a18-logic.py
```
2. Voltar à raiz A19 e executar os testes:
```bash
cd ..
python -B verificar.py
python -B ensaio-a19-logic.py
python -B academia_amostra.py
```
3. Ensaio manual com banco fictício:
```bash
python preparar_ensaio.py
python backup_sqlite.py dados-ensaio/sorveteria-ficticia.db dados-ensaio/sorveteria-ficticia-backup.db
```
O segundo comando exige que o destino ainda não exista. Para repetir, escolha outro nome de destino; não apague uma cópia anterior automaticamente.

## Saída de referência dos testes
O verificador A19 termina com:
```text
T05 — destino novo, backup API, integridade e registros conhecidos: OK
T05 — origem preservada após a cópia: OK
T05 — destino existente recusado e bytes anteriores preservados: OK
T06 — origem ausente recusada sem criar banco vazio: OK
T07 — origem igual ao destino recusada; dados originais intactos: OK
Todos os testes A19 passaram.
```

## Limites
Os testes automatizados não substituem demonstração presencial da GUI, navegação por Tab/Shift+Tab, inspeção de foco/redimensionamento nem feedback real de colega/professor. Esses itens foram deixados como pendência para A20, sem declarar execução que não ocorreu.
