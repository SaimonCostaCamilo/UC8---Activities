# Relatório da Aula 08 — Carrinho, pagamento e arredondamento decimal

**Aluno:** Saimon Costa Camilo  
**Turma:** TDS  
**Data do relatório:** 12/11/2026

## 1. Objetivo da atividade

Adicionar regras de pagamento ao pedido da sorveteria, calculando descontos e arredondamentos monetários sem alterar os itens do carrinho.

## 2. Arquivos e organização do projeto

- `main.py`: interface do carrinho e seleção da forma de pagamento.
- `modelos.py`: produtos, itens e pedido.
- `pagamento.py`: validação e cálculo do pagamento.
- `verificar.py`: testes automatizados.

## 3. Conceitos e decisões técnicas

- Usar `Decimal` e `ROUND_HALF_UP` para cálculos monetários.
- Aplicar fatores de pagamento sobre o subtotal original, evitando descontos acumulados.
- Manter a função de pagamento independente da interface e sem mutar o pedido.
- Validar forma de pagamento e valores monetários.

## 4. Execução e evidências

O registro A08 relata resultados observados para os casos iniciais: R$ 100,00 gera R$ 87,00 em dinheiro/PIX, R$ 92,00 no débito e R$ 100,00 no crédito em uma vez; R$ 0,50 em PIX resulta em R$ 0,44 com arredondamento HALF_UP. Também descreve repetição de chamadas e alternância de formas de pagamento sem alterar os itens.

## 5. Dificuldades, correções e pontos de atenção

Conferir o restante da matriz e o checklist integralmente no registro. Executar `python verificar.py` na pasta da aula para repetir os testes na versão entregue.

## 6. Conclusão

A atividade contribui para a evolução gradual do projeto da UC8. Este relatório foi elaborado a partir dos arquivos, README e registros existentes nesta pasta. Os testes são considerados concluídos somente quando há evidência explícita de execução; itens sem resultado observado permanecem identificados como pendentes, evitando registrar como realizado algo que não está comprovado.
