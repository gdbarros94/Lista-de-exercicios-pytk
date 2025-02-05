from models.funcionario_model import FuncionarioModel
from views.funcionario_view import FuncionarioView
from tkinter import messagebox

class FuncionarioController:
    def __init__(self, master, db_manager):
        self.model = FuncionarioModel(db_manager)
        self.view = FuncionarioView(master)
        
        # Bind dos eventos
        self.view.bind("<<SalvarFuncionario>>", self.salvar_funcionario)
        self.view.bind("<<BuscarFuncionario>>", self.buscar_funcionario)
        self.view.bind("<<SelecionarFuncionario>>", self.selecionar_funcionario)
        
        # Carrega dados iniciais
        self.atualizar_tabela()
    
    def salvar_funcionario(self, event=None):
        if not self.view.validar():
            return
            
        dados = self.view.obter_dados()
        if self.model.criar(dados):
            self.view.limpar_campos()
            self.atualizar_tabela()
            messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")
    
    def buscar_funcionario(self, event=None):
        cpf = self.view.widgets['CPF'].get()
        funcionario = self.model.buscar_por_cpf(cpf)
        
        if funcionario:
            for campo, valor in funcionario.items():
                if campo in self.view.widgets:
                    self.view.widgets[campo].set(valor)
        else:
            messagebox.showinfo("Busca", "Funcionário não encontrado!")
    
    def selecionar_funcionario(self, event=None):
        item = self.view.tabela.selection()[0]
        funcionario = self.view.tabela.item(item)['values']
        
        # Preenche o formulário com os dados do funcionário selecionado
        campos = ['Nome', 'CPF', 'Cargo', 'Departamento']
        for i, campo in enumerate(campos):
            self.view.widgets[campo].set(funcionario[i+1])
    
    def atualizar_tabela(self):
        funcionarios = self.model.listar_todos()
        self.view.preencher_tabela(funcionarios) 