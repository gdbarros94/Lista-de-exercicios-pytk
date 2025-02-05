import tkinter as tk
from tkinter import ttk, messagebox
from views.base import FormularioBase
from tkcalendar import DateEntry
from datetime import datetime

class FuncionarioView(FormularioBase):
    def __init__(self, master):
        campos = [
            {"label": "Nome", "tipo": "entry"},
            {"label": "CPF", "tipo": "entry"},
            {"label": "Cargo", "tipo": "entry"},
            {"label": "Departamento", "tipo": "combobox", 
             "opcoes": ["RH", "TI", "Financeiro", "Comercial"]},
            {"label": "Email", "tipo": "entry"},
            {"label": "Data Contratação", "tipo": "date"}
        ]
        super().__init__(master, campos)
        self.criar_botoes()
        self.criar_tabela()
        
    def criar_formulario(self):
        for i, campo in enumerate(self.campos):
            label = tk.Label(self, text=campo["label"])
            label.grid(row=i, column=0, padx=5, pady=5)
            
            if campo["tipo"] == "entry":
                widget = ttk.Entry(self)
            elif campo["tipo"] == "combobox":
                widget = ttk.Combobox(self, values=campo.get("opcoes", []))
            elif campo["tipo"] == "date":
                widget = DateEntry(self, width=12, background='darkblue',
                                 foreground='white', borderwidth=2)
            
            widget.grid(row=i, column=1, padx=5, pady=5)
            self.widgets[campo["label"]] = widget
    
    def criar_botoes(self):
        frame_botoes = ttk.Frame(self)
        frame_botoes.grid(row=len(self.campos), column=0, columnspan=2, pady=10)
        
        ttk.Button(frame_botoes, text="Salvar", 
                  command=lambda: self.event_generate("<<SalvarFuncionario>>")).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes, text="Buscar por CPF", 
                  command=lambda: self.event_generate("<<BuscarFuncionario>>")).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes, text="Limpar", 
                  command=self.limpar_campos).pack(side=tk.LEFT, padx=5)
    
    def criar_tabela(self):
        columns = ("ID", "Nome", "CPF", "Cargo", "Departamento", "Status")
        self.tabela = ttk.Treeview(self, columns=columns, show='headings')
        
        for col in columns:
            self.tabela.heading(col, text=col)
            self.tabela.column(col, width=100)
        
        self.tabela.grid(row=len(self.campos)+1, column=0, columnspan=2, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tabela.yview)
        scrollbar.grid(row=len(self.campos)+1, column=2, sticky='ns')
        self.tabela.configure(yscrollcommand=scrollbar.set)
        
        self.tabela.bind("<Double-1>", lambda e: self.event_generate("<<SelecionarFuncionario>>"))
    
    def preencher_tabela(self, dados):
        for item in self.tabela.get_children():
            self.tabela.delete(item)
            
        for funcionario in dados:
            status = "Ativo" if funcionario['ativo'] else "Inativo"
            self.tabela.insert("", tk.END, values=(
                funcionario['id'],
                funcionario['nome'],
                funcionario['cpf'],
                funcionario['cargo'],
                funcionario['departamento'],
                status
            ))
    
    def obter_dados(self):
        dados = super().obter_dados()
        dados['data_contratacao'] = self.widgets['Data Contratação'].get_date()
        return dados
    
    def limpar_campos(self):
        for widget in self.widgets.values():
            if hasattr(widget, 'delete'):
                widget.delete(0, tk.END)
            elif hasattr(widget, 'set'):
                widget.set('')
    
    def validar(self):
        dados = self.obter_dados()
        if not all(dados.values()):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return False
        return True 