"""Smoke test da janela A19; execute em desktop ou com xvfb-run."""
from pathlib import Path
import tempfile
from repositorio_academia import RepositorioAcademia
from academia_ui import AcademiaApp
from tkinter import messagebox


def verificar_interface():
    with tempfile.TemporaryDirectory(prefix='a19_gui_') as pasta:
        repo = RepositorioAcademia(Path(pasta) / 'academia.db')
        app = AcademiaApp(repo)
        try:
            app.root.update_idletasks(); app.root.update()
            assert app.root.winfo_exists()
            assert app.root.winfo_width() >= 720 and app.root.winfo_height() >= 520
            app.aluno_nome.insert(0, 'Lia GUI')
            app.adicionar_aluno()
            app.plano_nome.insert(0, 'Plano GUI')
            app.plano_valor.insert(0, '89,90')
            app.adicionar_plano()
            aluno_id = repo.listar_alunos()[0][0]
            plano_id = repo.listar_planos()[0][0]
            # Erro de formulário é apresentado sem gravar; suprime apenas a caixa modal no teste.
            app.m_aluno.insert(0, '999'); app.m_plano.insert(0, str(plano_id))
            original = messagebox.showerror; messagebox.showerror = lambda *a, **k: None
            try: app.adicionar_matricula()
            finally: messagebox.showerror = original
            assert len(repo.listar_matriculas()) == 0 and 'não encontrado' in app.status.get()
            app.m_aluno.delete(0, 'end'); app.m_aluno.insert(0, str(aluno_id))
            app.adicionar_matricula()
            app.root.update_idletasks(); app.root.update()
            assert len(app.alunos.get_children()) == 1
            assert len(app.planos.get_children()) == 1
            assert len(app.matriculas.get_children()) == 1
            app.root.geometry('800x560'); app.root.update_idletasks(); app.root.update()
            assert app.root.winfo_width() >= 720
            app.aluno_nome.focus_force(); app.root.update()
            antes = app.root.focus_get(); app.root.event_generate('<Tab>'); app.root.update()
            depois_tab = app.root.focus_get(); app.root.event_generate('<Shift-Tab>'); app.root.update()
            depois_shift = app.root.focus_get()
            assert antes is not None and depois_tab != antes and depois_shift == antes
            print('A19 GUI — janela, cadastros, erro/correção, Tab/Shift+Tab e redimensionamento: OK')
        finally:
            app.root.destroy()

if __name__ == '__main__':
    verificar_interface()
