# Ensaio isolado: cancelar não apaga; confirmar apaga.
cadastros = {12: "Copo azul"}
confirmou = False  # primeiro preveja a saída; depois altere para True
if confirmou:
    del cadastros[12]
print(cadastros)
