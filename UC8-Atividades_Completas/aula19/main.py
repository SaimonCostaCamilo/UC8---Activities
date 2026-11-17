"""Ponto de entrada da interface gráfica A19."""
from pathlib import Path
from repositorio_academia import RepositorioAcademia
from academia_ui import AcademiaApp

if __name__ == '__main__':
    banco = Path(__file__).resolve().parent / 'dados' / 'academia-a19.db'
    AcademiaApp(RepositorioAcademia(banco)).executar()
