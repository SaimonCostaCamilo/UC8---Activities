# Relatório da Aula 13 — Comprovante confirmado, exportação CSV e perfis

**Aluno:** Saimon Costa Camilo  
**Turma:** TDS  
**Data do relatório:** 12/11/2026

## 1. Objetivo da atividade

Separar a confirmação da venda da exportação de relatórios, preservar um retrato imutável do comprovante e demonstrar permissões por perfil.

## 2. Arquivos e organização do projeto

- `main.py`: interface principal.
- `pizzaria_main.py` e `sorveteria_main.py`: configurações da aplicação para catálogos distintos.
- `modelos.py` e `pagamento.py`: domínio e cálculos.
- `arquivos.py`: catálogo JSON.
- `relatorios.py`: exportação CSV.
- `perfis.py`: sessão demonstrativa.
- `verificar.py` e `verificar_interface.py`: testes de domínio e integração.

## 3. Conceitos e decisões técnicas

- Exportar somente comprovante confirmado, sem reler os widgets atuais.
- Gravar CSV em temporário e substituir o destino somente após escrita completa.
- Preservar o CSV anterior em caso de falha.
- Distinguir identificação demonstrativa, autenticação real e autorização.
- Reutilizar o mesmo fluxo para Mercado/Pizzaria/Sorveteria.

## 4. Execução e evidências

O registro A13 apresenta uma matriz detalhada de testes de domínio e integração Tkinter. Descreve a leitura de volta do CSV com caracteres especiais, valores em centavos, preservação do comprovante, cancelamento do seletor, falhas de escrita, perfis e transferência entre catálogos. Também documenta que a cópia original da A12 não veio no ZIP-base da A13, sem reconstruí-la artificialmente.

## 5. Dificuldades, correções e pontos de atenção

A apresentação visual ao professor continua sendo uma atividade local. Os testes automatizados de domínio e integração descritos no registro não substituem a conferência presencial dos fluxos.

## 6. Conclusão

A atividade contribui para a evolução gradual do projeto da UC8. Este relatório foi elaborado a partir dos arquivos, README e registros existentes nesta pasta. Os testes são considerados concluídos somente quando há evidência explícita de execução; itens sem resultado observado permanecem identificados como pendentes, evitando registrar como realizado algo que não está comprovado.
