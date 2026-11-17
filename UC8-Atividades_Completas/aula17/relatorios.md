# Relatório A17 — Sorveteria integrada e comparação visual

**Aluno:** Saimon Costa Camilo  
**Turma:** TDS  
**Data:** 12/11/2026

## Objetivo
Integrar o fluxo de venda ao SQLite sem persistir a montagem antes da confirmação. O cabeçalho e os itens precisam ser uma única unidade transacional; a falha em qualquer item deve desfazer toda a tentativa.

## Implementação realizada
- Reutilizados os modelos de produto, item e pedido, mantendo quantidades, subtotais, total e comprovante independentes da interface.
- Preservados os módulos de pagamento decimal, JSON, CSV e sessão de demonstração.
- Ampliado o esquema SQLite com `vendas` e `itens_venda`, IDs, chaves estrangeiras e snapshots de nome/preço do momento da venda.
- Ativadas chaves estrangeiras em toda conexão e bloqueadas exclusões de clientes/produtos já vinculados.
- Implementada gravação com `BEGIN IMMEDIATE`, inserção do cabeçalho e laço dos itens dentro da mesma transação; exceções provocam rollback.
- Controller valida estado, confirmação e versão da prévia; só finaliza o pedido depois do retorno bem-sucedido do repositório.
- Catálogo é conferido no momento da venda. Alteração de nome/preço ou produto ausente impede confirmação até revisão da montagem.
- Interface Tkinter organiza nova venda, cadastro de produtos, clientes, histórico, prévia e exportação CSV.
- Comparação CustomTkinter é opcional e isolada do núcleo.

## Organização dos arquivos
`main.py`, `controller.py`, `repositorio.py`, `memoria.py`, `modelos.py`, `pagamento.py`, `arquivos.py`, `relatorios.py`, `perfis.py`, `comparar_ctk.py`, `verificar.py` e `registro-a17.md`.

## Verificações executadas
Comando: `python -B verificar.py`.

Resultado observado: **Todos os casos automatizados A14 + A15 + A16 + A17 foram aprovados.** Foram verificados persistência e reabertura de cadastros, preço alterado, cliente inválido, o caso exigido de duas unidades a R$ 6,50 no PIX (R$ 13,00 → R$ 11,31), finalização única, falha real na segunda inserção com rollback, bloqueio de exclusões vinculadas e CSV baseado no comprovante.

O teste de rollback criou um trigger temporário para provocar uma falha durante a gravação do segundo item. A consulta posterior confirmou que não ficou venda parcial e que a montagem permaneceu aberta.

## Evidências e limitações
Os testes automatizados foram executados em banco e arquivos temporários. A janela Tkinter foi implementada, mas a conferência visual e de navegação por teclado depende de execução manual em ambiente desktop. A comparação CustomTkinter também permanece pendente de execução com a dependência instalada. Esses pontos não foram registrados como concluídos.

## Conclusão
O núcleo da A17 está integrado e passou pelos testes automatizados. O fluxo mantém a montagem em memória, persiste a venda inteira ou nada, exige revisão quando o catálogo muda e exporta o comprovante confirmado. A etapa restante é a validação manual da interface e, opcionalmente, da comparação visual.
