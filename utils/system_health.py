import mysql.connector
from mysql.connector import Error
import logging
import os
from datetime import datetime
import threading
import time

class SystemHealth:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.setup_logging()
        self.running = True
        try:
            self.health_thread = threading.Thread(target=self.monitor_health, daemon=True)
            self.health_thread.start()
        except Exception as e:
            logging.error(f"Erro ao iniciar thread de monitoramento: {e}")
        
    def setup_logging(self):
        """Configura o sistema de logging"""
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        logging.basicConfig(
            filename=f'logs/system_{datetime.now().strftime("%Y%m%d")}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def check_database_connection(self):
        """Verifica e tenta recuperar a conexão com o banco de dados"""
        try:
            connection = self.db_manager.conectar()
            if connection:
                logging.info("Conexão com banco de dados OK")
                return True
        except Error as e:
            logging.error(f"Erro na conexão com banco: {e}")
            self.try_recover_database()
            return False
            
    def try_recover_database(self):
        """Tenta recuperar a conexão com o banco de dados"""
        max_attempts = 3
        attempt = 0
        
        while attempt < max_attempts:
            try:
                logging.info(f"Tentativa {attempt + 1} de reconexão com o banco")
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="gestao_pessoal"
                )
                if connection:
                    logging.info("Reconexão bem sucedida")
                    connection.close()
                    return True
            except Error as e:
                attempt += 1
                logging.error(f"Falha na tentativa {attempt}: {e}")
                time.sleep(2)  # Espera 2 segundos antes da próxima tentativa
                
        return False
        
    def check_table_integrity(self):
        """Verifica a integridade das tabelas"""
        required_tables = ['Funcionarios', 'Contratos', 'Folha_Pagamento']
        
        try:
            for table in required_tables:
                query = f"SHOW TABLES LIKE '{table}'"
                result = self.db_manager.executar_consulta(query)
                if not result:
                    logging.error(f"Tabela {table} não encontrada")
                    self.try_recover_table(table)
        except Exception as e:
            logging.error(f"Erro ao verificar tabelas: {e}")
            
    def try_recover_table(self, table_name):
        """Tenta recuperar uma tabela ausente"""
        table_schemas = {
            'Funcionarios': """
                CREATE TABLE Funcionarios (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    nome VARCHAR(100) NOT NULL,
                    cpf VARCHAR(14) UNIQUE NOT NULL,
                    cargo VARCHAR(50),
                    departamento VARCHAR(50),
                    email VARCHAR(100),
                    data_contratacao DATE,
                    ativo BOOLEAN DEFAULT TRUE
                )
            """,
            'Contratos': """
                CREATE TABLE Contratos (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    funcionario_id INT,
                    tipo_contrato ENUM('CLT', 'PJ', 'Estágio'),
                    salario DECIMAL(10,2),
                    data_inicio DATE,
                    data_fim DATE,
                    multa_rescisoria DECIMAL(10,2) DEFAULT 0,
                    FOREIGN KEY (funcionario_id) REFERENCES Funcionarios(id)
                )
            """,
            'Folha_Pagamento': """
                CREATE TABLE Folha_Pagamento (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    funcionario_id INT,
                    mes_ano DATE,
                    horas_trabalhadas INT,
                    valor_pago DECIMAL(10,2),
                    descontos DECIMAL(10,2) DEFAULT 0,
                    beneficios DECIMAL(10,2) DEFAULT 0,
                    FOREIGN KEY (funcionario_id) REFERENCES Funcionarios(id)
                )
            """
        }
        
        try:
            if table_name in table_schemas:
                self.db_manager.executar_comando(table_schemas[table_name])
                logging.info(f"Tabela {table_name} recuperada com sucesso")
        except Exception as e:
            logging.error(f"Erro ao recuperar tabela {table_name}: {e}")
            
    def monitor_health(self):
        """Monitor contínuo de saúde do sistema"""
        while self.running:
            try:
                self.check_database_connection()
                self.check_table_integrity()
            except Exception as e:
                logging.error(f"Erro no monitoramento: {e}")
            finally:
                time.sleep(60)  # Verifica a cada minuto
            
    def stop_monitoring(self):
        """Para o monitoramento"""
        try:
            self.running = False
            if hasattr(self, 'health_thread'):
                self.health_thread.join(timeout=1.0)  # Timeout de 1 segundo
        except Exception as e:
            logging.error(f"Erro ao parar monitoramento: {e}") 