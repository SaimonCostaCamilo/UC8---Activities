# Teoria A20 — vínculos, recuperação e entrega

## Conceitos obrigatórios
- Um vínculo usa IDs; corrigir o nome não altera a identidade.
- Referência órfã aponta para registro inexistente e deve ser recusada.
- Em memória, conferir se os IDs referenciados existem antes de aceitar a operação.
- No SQLite, declarar chaves estrangeiras e executar `PRAGMA foreign_keys=ON` em cada conexão.
- `ON DELETE RESTRICT` bloqueia exclusão de registro ainda referenciado.
- Recuperação exige nova tentativa individual após apoio e evidência observável.
- Entrega deve identificar arquivos, comandos, dados, resultados e limites reproduzíveis.

## Exemplo mínimo e resultado esperado
Arquivo: `ensaio-a20-logic.py`

```text
True
True
False
```

A primeira e segunda saídas permanecem verdadeiras porque só o nome mudou. A terceira é falsa porque `aluno_id` foi trocado para 99, inexistente.

## Retomada rápida — tópicos para responder de memória
- Backup existente não prova, sozinho, recuperação: é preciso abrir a cópia, conferir integridade e dados conhecidos.
- A pergunta técnica individual evidencia compreensão e capacidade de justificar uma decisão com código e teste.
- Um contrato de repositório pode ser definido por comportamento/protocolo; herança não é obrigatória.
- Identidade (ID) e confirmação são decisões separadas: o ID seleciona o registro certo; a confirmação protege contra exclusão acidental.
