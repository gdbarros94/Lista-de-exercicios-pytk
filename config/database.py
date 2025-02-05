import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
import logging

class GerenciadorBancoDados:
    def __init__(self):
        self.conexao = None
        self.cursor = None
        
    def conectar(self):
        if self.conexao and self.conexao.is_connected():
            return self.conexao
            
        try:
            self.conexao = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="test"  # ou o nome do seu banco
            )
            return self.conexao
        except Error as e:
            logging.error(f"Erro de conexão com o banco: {e}")
            messagebox.showerror("Erro de Conexão", 
                               f"Não foi possível conectar ao banco. Verifique se o MySQL está rodando.")
            return None
            
    def executar_consulta(self, query, params=None):
        try:
            self.conectar()
            self.cursor = self.conexao.cursor(dictionary=True)
            self.cursor.execute(query, params or ())
            resultado = self.cursor.fetchall()
            return resultado
        except Error as e:
            messagebox.showerror("Erro na Consulta", f"Falha ao executar consulta: {e}")
            return []
        finally:
            self.fechar_conexao()
            
    def executar_comando(self, query, params=None):
        try:
            self.conectar()
            self.cursor = self.conexao.cursor()
            self.cursor.execute(query, params or ())
            self.conexao.commit()
            return True
        except Error as e:
            messagebox.showerror("Erro no Comando", f"Falha ao executar comando: {e}")
            return False
        finally:
            self.fechar_conexao()
            
    def iniciar_transacao(self):
        self.conectar()
        self.conexao.start_transaction()
        
    def confirmar_transacao(self):
        if self.conexao:
            self.conexao.commit()
            
    def reverter_transacao(self):
        if self.conexao:
            self.conexao.rollback()
            
    def fechar_conexao(self):
        if self.cursor:
            self.cursor.close()
        if self.conexao:
            self.conexao.close() 