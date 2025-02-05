import tkinter as tk
from tkinter import messagebox  # Corrigido: importação correta do messagebox
from controllers.base import GerenciadorJanelas
from config.database import GerenciadorBancoDados
from utils.system_health import SystemHealth
import sys
import traceback
import logging
from controllers.funcionario_controller import FuncionarioController

class MainApp:
    def __init__(self):
        # Configurando logging primeiro
        self.setup_logging()
        
        # Inicializando interface gráfica
        self.root = tk.Tk()
        self.root.title("Sistema de Gestão de Pessoal")
        self.root.geometry("800x600")
        
        try:
            # Inicializando componentes
            self.db_manager = GerenciadorBancoDados()
            self.system_health = SystemHealth(self.db_manager)
            self.gerenciador = GerenciadorJanelas(self.root)
            
            # Inicializando controladores
            self.funcionario_controller = FuncionarioController(self.root, self.db_manager)
            
            # Configurando a interface
            self.configurar_interface()
            
            # Mostrar frame inicial
            self.gerenciador.mostrar_frame("Funcionarios")
            
        except Exception as e:
            logging.error(f"Erro na inicialização: {e}")
            messagebox.showerror("Erro", f"Erro ao inicializar o sistema: {e}")
        
        # Configurando tratamento global de exceções
        sys.excepthook = self.handle_exception
        
        # Configurando evento de fechamento
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def configurar_interface(self):
        # Criar menu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Cadastros
        cadastros_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Cadastros", menu=cadastros_menu)
        cadastros_menu.add_command(label="Funcionários", 
                                 command=lambda: self.gerenciador.mostrar_frame("Funcionarios"))
        
        # Configurar frames
        self.gerenciador.adicionar_frame("Funcionarios", self.funcionario_controller.view)
    
    def testar_conexao(self):
        """Função para testar a conexão com o banco"""
        try:
            if self.db_manager.conectar():
                messagebox.showinfo("Sucesso", "Conexão com o banco estabelecida!")
            else:
                messagebox.showerror("Erro", "Não foi possível conectar ao banco")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao testar conexão: {e}")
        
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """Tratamento global de exceções não capturadas"""
        error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        logging.error(f"Exceção não tratada: {error_msg}")
        
        # Tenta recuperar o sistema
        self.system_health.check_database_connection()
        
        # Mostra mensagem ao usuário
        messagebox.showerror(
            "Erro no Sistema",
            "Ocorreu um erro inesperado. O sistema tentará se recuperar automaticamente."
        )
        
    def on_closing(self):
        """Manipula o fechamento adequado do sistema"""
        try:
            if hasattr(self, 'system_health'):
                self.system_health.stop_monitoring()
            self.root.destroy()
        except Exception as e:
            logging.error(f"Erro ao fechar aplicação: {e}")
            self.root.destroy()
        
    def iniciar(self):
        try:
            self.root.mainloop()
        except Exception as e:
            logging.error(f"Erro na execução principal: {e}")
            self.on_closing()

if __name__ == "__main__":
    app = MainApp()
    app.iniciar() 