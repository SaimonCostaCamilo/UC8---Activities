"""Ponto de entrada da A20: interface A19 com repositório relacional integrado."""
from pathlib import Path
import sys
A19 = Path(__file__).resolve().parents[1] / 'aula19'
sys.path.insert(0, str(A19))
from academia_ui import AcademiaApp
from repositorio_relacional import RepositorioRelacional

if __name__ == '__main__':
    banco = Path(__file__).resolve().parent / 'dados' / 'academia-a20.db'
    AcademiaApp(RepositorioRelacional(banco), 'Academia — A20 (relacionamentos SQLite)').executar()
