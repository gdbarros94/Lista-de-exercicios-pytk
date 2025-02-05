from datetime import date

class FuncionarioModel:
    def __init__(self, db_manager):
        self.db = db_manager
        
    def criar(self, dados):
        query = """
        INSERT INTO Funcionarios 
        (nome, cpf, cargo, departamento, email, data_contratacao, ativo)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            dados['nome'],
            dados['cpf'],
            dados['cargo'],
            dados['departamento'],
            dados['email'],
            dados['data_contratacao'],
            True
        )
        return self.db.executar_comando(query, params)
        
    def buscar_por_cpf(self, cpf):
        query = "SELECT * FROM Funcionarios WHERE cpf = %s"
        resultado = self.db.executar_consulta(query, (cpf,))
        return resultado[0] if resultado else None
        
    def listar_todos(self):
        query = "SELECT * FROM Funcionarios"
        return self.db.executar_consulta(query)
        
    def atualizar(self, id, dados):
        query = """
        UPDATE Funcionarios 
        SET nome = %s, cargo = %s, departamento = %s, 
            email = %s, ativo = %s
        WHERE id = %s
        """
        params = (
            dados['nome'],
            dados['cargo'],
            dados['departamento'],
            dados['email'],
            dados['ativo'],
            id
        )
        return self.db.executar_comando(query, params)
        
    def desativar(self, id):
        query = "UPDATE Funcionarios SET ativo = False WHERE id = %s"
        return self.db.executar_comando(query, (id,)) 