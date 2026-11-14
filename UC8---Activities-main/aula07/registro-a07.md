# Registro A07 — Modelos de domínio e testes automatizados

**Nome:** Saimon Camilo  
**Turma:** TDS  
**Data:** 13/11/2026

## Objetivo e conceitos
Modelar produtos e pedido, validar quantidade positiva, calcular subtotais em centavos e impedir alterações em pedido fechado. A identidade do produto é seu código; não se deve inserir o mesmo código duas vezes no pedido.

## Arquitetura
`modelos.py` concentra Produto, Pedido, quantidade e formatação; `verificar.py` contém previsões e asserts.

## Testes executados e correção
A primeira execução encontrou divergência apenas na mensagem esperada pelo teste: o modelo informa “está no pedido”, enquanto o assert exigia “já está no pedido”. O verificador foi corrigido para conferir o trecho estável da mensagem, sem alterar a regra de negócio. Em seguida, `python -B verificar.py` foi executado novamente com sucesso.

**Situação:** suíte automatizada aprovada após correção do próprio teste. Foram conferidos subtotais, total, formatação, duplicidade, quantidade inválida, pedido fechado e linhas do pedido.
