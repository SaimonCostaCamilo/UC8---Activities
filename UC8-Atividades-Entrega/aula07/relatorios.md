# Relatório da Aula 07 — Sorveteria: produtos, itens e pedido

**Aluno:** Saimon Costa Camilo  
**Turma:** TDS  
**Data do relatório:** 12/11/2026

## 1. Objetivo da atividade

Modelar um catálogo de produtos e um pedido composto por itens, quantidades e subtotais, com identificação de produtos por código.

## 2. Arquivos e organização do projeto

- `modelos.py`: classes de domínio para produto, item e pedido.
- `verificar.py`: testes automatizados do modelo e das regras.

## 3. Conceitos e decisões técnicas

- Representar produto, item e pedido como objetos com responsabilidades distintas.
- Manter uma coleção própria em cada pedido.
- Somar quantidades quando o mesmo código é adicionado, sem confundir produtos diferentes que tenham o mesmo nome.
- Validar quantidades e recalcular o total a partir dos subtotais.

## 4. Execução e evidências

O registro A07 descreve oito casos previstos, incluindo cálculo de R$ 32,50 para os itens de exemplo, independência entre pedidos, identificação por código e validação de quantidade. O documento disponível não contém resultados observados preenchidos para esses casos; por isso, são apresentados como roteiro de validação, não como testes concluídos.

## 5. Dificuldades, correções e pontos de atenção

Executar `python verificar.py`, preencher cada previsão com o resultado observado e conferir a interface e o percurso por teclado, caso a interface esteja presente na versão local.

## 6. Conclusão

A atividade contribui para a evolução gradual do projeto da UC8. Este relatório foi elaborado a partir dos arquivos, README e registros existentes nesta pasta. Os testes são considerados concluídos somente quando há evidência explícita de execução; itens sem resultado observado permanecem identificados como pendentes, evitando registrar como realizado algo que não está comprovado.
