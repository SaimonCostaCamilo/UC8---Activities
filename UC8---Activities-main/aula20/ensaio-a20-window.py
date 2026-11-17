"""Ensaio para registrar uma revalidação sem inventar observações."""
registro = {
    "ação": "reabrir a aplicação em pasta limpa com banco fictício",
    "observação": "PREENCHER após executar; não presumir resultado",
    "pendência": "inspecionar GUI, Tab/Shift+Tab, foco e redimensionamento",
}
for parte, texto in registro.items():
    print(parte, "->", texto)
