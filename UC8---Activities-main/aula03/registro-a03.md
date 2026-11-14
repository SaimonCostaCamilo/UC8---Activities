# Registro A03 — Conversão de moedas e cálculos monetários

**Nome:** Saimon Camilo  
**Turma:** TDS  
**Data:** 13/11/2026

## Objetivo e conceitos
Converter valores usando cotações fictícias, manter juntos os dados e resultados de cada cálculo confirmado e impedir que uma tentativa inválida substitua o último resultado válido.

## Retomada
- Exibir deve consultar o último cálculo confirmado, não recalcular silenciosamente com campos editados.
- Um erro deve invalidar apenas a tentativa atual e preservar o último resultado válido.
- `get()` retorna texto; `int()` não representa valores decimais como `2.5`. Para cotação e moeda, usar conversão decimal apropriada e normalizar vírgula/ponto conforme a regra definida.

## Testes e evidências
A matriz usa cotações fictícias e cobre estado vazio, cálculo válido, edição sem confirmação e tentativa inválida após cálculo válido. O registro documenta que o cálculo confirmado é armazenado e a exibição consulta os resultados registrados.

**Situação:** evidências manuais documentadas; não há verificador automatizado nesta aula.
