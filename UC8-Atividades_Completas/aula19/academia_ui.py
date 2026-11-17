"""Interface Tkinter reutilizável pela A19 e pela A20."""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from backup_sqlite import criar_backup

class AcademiaApp:
    def __init__(self, repositorio, titulo='Academia — demonstração A19'):
        self.repo = repositorio
        self.root = tk.Tk()
        self.root.title(titulo)
        self.root.geometry('920x650')
        self.root.minsize(720, 520)
        self._montar()
        self.atualizar()

    def _montar(self):
        outer = ttk.Frame(self.root, padding=14)
        outer.pack(fill='both', expand=True)
        ttk.Label(outer, text=self.root.title(), font=('TkDefaultFont', 16, 'bold')).pack(anchor='w')
        ttk.Label(outer, text='Dados demonstrativos fictícios • IDs identificam os registros').pack(anchor='w', pady=(2, 12))
        self.tabs = ttk.Notebook(outer)
        self.tabs.pack(fill='both', expand=True)
        self.tab_alunos = ttk.Frame(self.tabs, padding=12)
        self.tab_planos = ttk.Frame(self.tabs, padding=12)
        self.tab_matriculas = ttk.Frame(self.tabs, padding=12)
        self.tab_backup = ttk.Frame(self.tabs, padding=12)
        self.tabs.add(self.tab_alunos, text='Alunos')
        self.tabs.add(self.tab_planos, text='Planos')
        self.tabs.add(self.tab_matriculas, text='Matrículas')
        self.tabs.add(self.tab_backup, text='Backup SQLite')
        self._aba_alunos(); self._aba_planos(); self._aba_matriculas(); self._aba_backup()
        self.status = tk.StringVar(value='Pronto. Use Tab/Shift+Tab para navegar.')
        ttk.Label(outer, textvariable=self.status, relief='sunken', anchor='w', padding=6).pack(fill='x', pady=(10, 0))
        self.root.bind('<F5>', lambda _e: self.atualizar())

    def _tree(self, parent, columns, headings):
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=12)
        for col, heading, width in headings:
            tree.heading(col, text=heading); tree.column(col, width=width, anchor='w')
        tree.grid(row=3, column=0, columnspan=3, sticky='nsew', pady=(8, 0))
        parent.rowconfigure(3, weight=1)
        return tree

    def _aba_alunos(self):
        f=self.tab_alunos
        ttk.Label(f,text='Nome do aluno').grid(row=0,column=0,sticky='w')
        self.aluno_nome=ttk.Entry(f,width=42); self.aluno_nome.grid(row=1,column=0,sticky='ew',padx=(0,8))
        ttk.Button(f,text='Cadastrar aluno',command=self.adicionar_aluno).grid(row=1,column=1)
        self.alunos=self._tree(f,('id','nome'),[('id','ID',90),('nome','Nome',500)])
        ttk.Button(f,text='Excluir aluno selecionado',command=self.excluir_aluno).grid(row=4,column=0,columnspan=3,sticky='e',pady=(6,0))
        f.columnconfigure(0,weight=1); self.aluno_nome.bind('<Return>',lambda _e:self.adicionar_aluno())

    def _aba_planos(self):
        f=self.tab_planos
        ttk.Label(f,text='Nome do plano').grid(row=0,column=0,sticky='w')
        ttk.Label(f,text='Valor (R$)').grid(row=0,column=1,sticky='w')
        self.plano_nome=ttk.Entry(f,width=34); self.plano_nome.grid(row=1,column=0,sticky='ew',padx=(0,8))
        self.plano_valor=ttk.Entry(f,width=16); self.plano_valor.grid(row=1,column=1,sticky='ew',padx=(0,8))
        ttk.Button(f,text='Cadastrar plano',command=self.adicionar_plano).grid(row=1,column=2)
        self.planos=self._tree(f,('id','nome','valor'),[('id','ID',80),('nome','Plano',400),('valor','Valor (R$)',160)])
        ttk.Button(f,text='Excluir plano selecionado',command=self.excluir_plano).grid(row=4,column=0,columnspan=3,sticky='e',pady=(6,0))
        f.columnconfigure(0,weight=1)

    def _aba_matriculas(self):
        f=self.tab_matriculas
        ttk.Label(f,text='ID do aluno').grid(row=0,column=0,sticky='w')
        ttk.Label(f,text='ID do plano').grid(row=0,column=1,sticky='w')
        self.m_aluno=ttk.Entry(f,width=16); self.m_aluno.grid(row=1,column=0,sticky='ew',padx=(0,8))
        self.m_plano=ttk.Entry(f,width=16); self.m_plano.grid(row=1,column=1,sticky='ew',padx=(0,8))
        ttk.Button(f,text='Criar matrícula',command=self.adicionar_matricula).grid(row=1,column=2)
        ttk.Label(f,text='A matrícula referencia os cadastros pelos IDs, não pelos nomes.').grid(row=2,column=0,columnspan=3,sticky='w',pady=(8,0))
        self.matriculas=self._tree(f,('id','aluno_id','aluno','plano_id','plano'),[
            ('id','Matrícula',85),('aluno_id','ID aluno',85),('aluno','Aluno',220),('plano_id','ID plano',85),('plano','Plano',220)])
        f.columnconfigure(0,weight=1); f.columnconfigure(1,weight=1)

    def _aba_backup(self):
        f=self.tab_backup
        ttk.Label(f,text='Crie uma cópia de segurança do banco atual em um destino novo.').pack(anchor='w',pady=(0,12))
        ttk.Button(f,text='Selecionar destino e criar backup',command=self.fazer_backup).pack(anchor='w')
        ttk.Label(f,text='O destino existente nunca é sobrescrito. A integridade da cópia é verificada.').pack(anchor='w',pady=8)

    def _executar(self, func):
        try:
            resultado=func(); self.atualizar(); self.status.set('Operação concluída com sucesso.')
            return resultado
        except Exception as erro:
            self.status.set(f'Operação não concluída: {erro}')
            messagebox.showerror('Não foi possível concluir',str(erro),parent=self.root)
            return None

    def adicionar_aluno(self):
        resultado=self._executar(lambda:self.repo.adicionar_aluno(self.aluno_nome.get()))
        if resultado is not None: self.aluno_nome.delete(0,'end'); self.status.set(f'Aluno cadastrado com ID {resultado}.')

    def adicionar_plano(self):
        def acao():
            texto=self.plano_valor.get().strip().replace(',','.')
            try: centavos=round(float(texto)*100)
            except ValueError: raise ValueError('Informe um valor monetário válido, por exemplo 99,90.')
            if centavos < 0: raise ValueError('O valor não pode ser negativo.')
            return self.repo.adicionar_plano(self.plano_nome.get(),centavos)
        resultado=self._executar(acao)
        if resultado is not None:
            self.plano_nome.delete(0,'end'); self.plano_valor.delete(0,'end'); self.status.set(f'Plano cadastrado com ID {resultado}.')

    def adicionar_matricula(self):
        def acao():
            try: aluno=int(self.m_aluno.get().strip()); plano=int(self.m_plano.get().strip())
            except ValueError: raise ValueError('Informe IDs numéricos inteiros.')
            return self.repo.adicionar_matricula(aluno,plano)
        resultado=self._executar(acao)
        if resultado is not None:
            self.m_aluno.delete(0,'end'); self.m_plano.delete(0,'end'); self.status.set(f'Matrícula criada com ID {resultado}.')

    @staticmethod
    def _id_selecionado(tree, rotulo):
        selecionados = tree.selection()
        if not selecionados:
            raise ValueError(f'Selecione um {rotulo} na tabela.')
        return int(tree.item(selecionados[0], 'values')[0])

    def excluir_aluno(self):
        self._executar(lambda: self.repo.excluir_aluno(self._id_selecionado(self.alunos, 'aluno')))

    def excluir_plano(self):
        self._executar(lambda: self.repo.excluir_plano(self._id_selecionado(self.planos, 'plano')))

    def fazer_backup(self):
        destino=filedialog.asksaveasfilename(parent=self.root,title='Salvar backup SQLite',defaultextension='.db',filetypes=[('Banco SQLite','*.db')])
        if not destino: self.status.set('Backup cancelado pelo usuário.'); return
        resultado=self._executar(lambda:criar_backup(self.repo.caminho,destino))
        if resultado: self.status.set(f'Backup íntegro criado em: {resultado}')

    def atualizar(self):
        for tree in (getattr(self,'alunos',None),getattr(self,'planos',None),getattr(self,'matriculas',None)):
            if tree:
                for item in tree.get_children(): tree.delete(item)
        if hasattr(self,'alunos'):
            for row in self.repo.listar_alunos(): self.alunos.insert('','end',values=row)
            for row in self.repo.listar_planos(): self.planos.insert('','end',values=(row[0],row[1],f'R$ {row[2]/100:.2f}'.replace('.',',')))
            for row in self.repo.listar_matriculas(): self.matriculas.insert('','end',values=row)

    def executar(self): self.root.mainloop()
