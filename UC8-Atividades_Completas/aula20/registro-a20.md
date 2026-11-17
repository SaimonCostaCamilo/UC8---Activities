# Meu registro A20 — Vínculos, recuperação e entrega final

**Nome/código individual:** Saimon Camilo  
**Turma:** TDS  
**Data:** 13/11/2026

## Arquitetura antes do código
- `main.py`: abre a janela A20 usando a interface Tkinter compartilhada da A19.
- `../aula19/academia_ui.py`: formulários, tabelas, eventos, mensagens e atualização visual.
- `repositorio_relacional.py`: persistência A20 com `PRAGMA foreign_keys=ON` em cada conexão e chaves estrangeiras `ON DELETE RESTRICT`.
- `vinculos.py`: valida IDs positivos, únicos e referências existentes em memória.
- `relacoes_sqlite.py`: demonstra as mesmas regras no mecanismo SQLite e rollback.
- `verificar.py`: testes de unidade e integração em banco temporário.
- `../aula19/referencia-a18/`: candidata desktop do projeto integrador preservada para revalidação separada.

## Matriz de execução automatizada

| Caso | Evidência executada | Resultado |
|---|---|---|
| T01 — vínculo válido e nome alterado | `validar_vinculos`; nome muda sem mudar ID | Aprovado |
| T02 — referência inexistente | aluno 99 e plano 88 recusados sem mutar coleções | Aprovado |
| T03 — IDs inválidos/duplicados | bool, negativo e IDs duplicados recusados | Aprovado |
| T04 — exclusão vinculada | `pode_excluir_aluno(41, ...)` retorna False | Aprovado |
| T05 — FK/RESTRICT | SQLite recusa referência órfã e exclusão vinculada | Aprovado |
| T06 — rollback | aluno e matrícula permanecem após erro; `integrity_check=ok` | Aprovado |
| T07 — integração do repositório | cadastro, matrícula, referência inexistente e exclusões protegidas testados no `RepositorioRelacional` | Aprovado |
| T08 — execução dos módulos | comandos documentados no README e scripts independentes | Aprovado por execução dos testes e imports |
| T09 — limites da evidência | documentação não marca inspeção presencial/feedback como concluídos | Aprovado |

Comando executado nesta revisão: `python -B verificar.py` na pasta `aula20`; todos os asserts passaram.

## Como executar a janela

```bash
python -B main.py
```

Cadastre aluno e plano, anote os IDs, crie matrícula usando esses IDs e confira a listagem. Tente usar um ID inexistente para observar a recusa. Se houver matrícula, tente excluir o aluno/plano pelo repositório: a regra bloqueia a exclusão. O teste automatizado cobre esse comportamento sem apagar dados reais.

## Inspeção manual da interface — preencher após executar
- [ ] Controles e rótulos conferidos:
- [ ] Percurso por Tab/Shift+Tab e acionamento por Enter:
- [ ] Mensagem após erro e possibilidade de corrigir:
- [ ] Redimensionamento e comportamento observado:
- [ ] Revalidação da candidata `aula19/referencia-a18/main.py` executada:
- [ ] Feedback real recebido (pessoa/contexto e comentário literal):

## Recuperação e reflexão individual
Dificuldade que encontrei:
Apoio efetivamente recebido:
Nova tentativa individual e evidência:
Decisão técnica que consigo explicar:
Próximo estudo:

## Entrega
Versão/pasta extraída e comando executado:
Caminho de banco fictício utilizado:
Cópia local do ZIP conferida:
Envio/recebimento no canal do curso (preencher somente após confirmação real):

## Limites
A automação valida regras de domínio, persistência e integridade referencial. Ela não comprova aparência em desktop, percurso real de teclado, apresentação individual, feedback externo ou recebimento do arquivo pelo professor. Esses itens dependem da execução e observação do aluno.
