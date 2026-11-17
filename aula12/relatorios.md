# Relatório da Aula 12 — Persistência de catálogo e exportação de dados

**Aluno:** Saimon Costa Camilo  
**Turma:** TDS  
**Data do relatório:** 12/11/2026

## 1. Objetivo da atividade

Evoluir a aplicação com leitura e gravação de catálogo em JSON, validação dos dados, cálculo monetário e testes de regressão.

## 2. Arquivos e organização do projeto

- `main.py`: interface da aplicação.
- `modelos.py`: classes de produto, item e pedido.
- `pagamento.py`: regras monetárias.
- `arquivos.py`: leitura, validação e gravação do catálogo JSON.
- `verificar.py`: testes automatizados.

## 3. Conceitos e decisões técnicas

- Diferenciar arquivo inexistente de arquivo existente com conteúdo inválido.
- Validar estrutura e conteúdo antes de utilizar os dados.
- Preservar o arquivo original quando a leitura ou gravação falhar.
- Manter cálculos monetários e estado do pedido coerentes.

## 4. Execução e evidências

O registro A12 e os módulos indicam a inclusão do tratamento de arquivos JSON junto ao projeto de venda. A verificação deve considerar os casos de arquivo ausente, válido e inválido, além da regressão de pagamento e modelo. O status final de cada caso deve ser lido na matriz do registro A12.

## 5. Dificuldades, correções e pontos de atenção

Executar `python verificar.py` e conferir os casos de arquivo em uma pasta temporária. O pacote atual mantém os arquivos da A12 fornecidos; não se deve substituir a versão original por uma reconstrução.

## 6. Conclusão

A atividade contribui para a evolução gradual do projeto da UC8. Este relatório foi elaborado a partir dos arquivos, README e registros existentes nesta pasta. Os testes são considerados concluídos somente quando há evidência explícita de execução; itens sem resultado observado permanecem identificados como pendentes, evitando registrar como realizado algo que não está comprovado.
