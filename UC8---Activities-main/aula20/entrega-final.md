# Minha entrega final — A20

**Identificação individual e data:** Saimon Costa Camilo · TDS · 17/11/2026  
**Versão/pasta enviada e cópia local:** preencher após conferir o ZIP extraído e a cópia local.

## Inventário

- `A20/`: scripts, README, registro e roteiro de revalidação.
- `A19/`: pacote anterior preservado, incluindo `referencia-a18/` (aplicação desktop candidata).
- Banco fictício SQLite de comparação: temporário, criado durante `relacoes_sqlite.py`.
- Ambientes, caches e bancos reais: não incluídos.

## Evidências individuais

- I1 — ambiente e reprodução: executar os comandos do `README-A20.md`; anotar versão Python e resultado observado.
- I2 — código e funcionalidades: `vinculos.py`, `relacoes_sqlite.py` e `verificar.py`; registrar saída real.
- I3 — interface, usabilidade e acessibilidade: inspeção manual da candidata desktop ainda requer execução em ambiente gráfico.
- I4 — eventos e validações: scripts verificam IDs, referências ausentes e exclusão vinculada; GUI deve ser inspecionada separadamente.

## Recuperação

Dificuldade delimitada: inspeção manual da GUI e percurso por teclado/foco, pendência anotada na A19.  
Apoio recebido: preencher com apoio real recebido; não presumir.  
Nova tentativa individual e evidência: preencher após executar roteiro-revalidacao-a19.md.  
O que ainda não foi observado: GUI, Tab/Shift+Tab, foco, redimensionamento e feedback externo até que sejam executados.

## Vínculos

- IDs válidos: aluno 41, plano 7, matrícula 101.
- Referência inexistente: aluno 99 ou plano 88 deve ser recusado.
- Exclusão vinculada: aluno 41 não pode ser excluído enquanto matrícula 101 existir.
- JSON/memória: validação explícita pelo código antes de aceitar os registros.
- SQLite: `PRAGMA foreign_keys=ON` por conexão e `ON DELETE RESTRICT`; erro de integridade deve ser seguido de rollback.

## Entrega

Downloads/arquivos executados conferidos: preencher após conferência.  
Recebimento no canal combinado: preencher somente após confirmação real.  
Autoavaliação e próximo estudo: preencher individualmente.

## Conferência em pasta limpa

Comando executado pelo README:
Dados fictícios e caminho realmente usados:
Resultado do fluxo válido e da recusa:
Correção demonstrada e evidência da nova tentativa:
Limite que outro usuário precisa conhecer:

## Alterações desde A19

A19 foi preservada sem alterações. Esta A20 acrescenta ensaio de integridade de vínculos por ID, comparação com chaves estrangeiras SQLite e documentação da entrega. A candidata desktop segue separada e não foi automaticamente integrada aos exemplos A20.
