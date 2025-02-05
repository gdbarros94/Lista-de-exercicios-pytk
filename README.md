**LISTA DE EXERCÍCIOS FINAL: SISTEMA DE GESTÃO DE PESSOAL COM PYTHON/TKINTER**  
*(Versão Aprimorada e Detalhada)*  

---

### **Exercício 1: Criação do Banco de Dados**  
**Objetivo:** Preparar a estrutura do banco de dados MySQL.  
**Tarefas:**  
1. Crie o banco `gestao_pessoal` (local via XAMPP ou remoto).  
2. Execute estas queries:  
   ```sql  
   -- Funcionários (adicione departamento e email)  
   CREATE TABLE Funcionarios (
       id INT PRIMARY KEY AUTO_INCREMENT,
       nome VARCHAR(100) NOT NULL,
       cpf VARCHAR(14) UNIQUE NOT NULL,
       cargo VARCHAR(50),
       departamento VARCHAR(50),
       email VARCHAR(100),
       data_contratacao DATE,
       ativo BOOLEAN DEFAULT TRUE
   );

   -- Contratos (adicione cláusula de multa rescisória)  
   CREATE TABLE Contratos (
       id INT PRIMARY KEY AUTO_INCREMENT,
       funcionario_id INT,
       tipo_contrato ENUM('CLT', 'PJ', 'Estágio'),
       salario DECIMAL(10,2),
       data_inicio DATE,
       data_fim DATE,
       multa_rescisoria DECIMAL(10,2) DEFAULT 0,
       FOREIGN KEY (funcionario_id) REFERENCES Funcionarios(id)
   );

   -- Folha_Pagamento (adicione descontos e benefícios)  
   CREATE TABLE Folha_Pagamento (
       id INT PRIMARY KEY AUTO_INCREMENT,
       funcionario_id INT,
       mes_ano DATE,
       horas_trabalhadas INT,
       valor_pago DECIMAL(10,2),
       descontos DECIMAL(10,2) DEFAULT 0,
       beneficios DECIMAL(10,2) DEFAULT 0,
       FOREIGN KEY (funcionario_id) REFERENCES Funcionarios(id)
   );
   ```  
**Importante:** Sem este banco, o sistema não funcionará! Use o PHPMyAdmin para validação.

---

### **Exercício 2: Classe de Conexão ao Banco (Superclasse)**  
**Objetivo:** Criar `GerenciadorBancoDados` com transações e tratamento de erros.  
**Tarefas:**  
1. Implemente métodos:  
   - `conectar()`: Retorna uma conexão usando `mysql.connector`.  
   - `executar_consulta(query, params)`: Para SELECTs (retorna lista de dicionários).  
   - `executar_comando(query, params)`: Para INSERT/UPDATE/DELETE (com `commit` automático).  
   - `iniciar_transacao()`, `confirmar_transacao()`, `reverter_transacao()`.  
2. Exemplo de tratamento de erro:  
   ```python  
   try:
       db.executar_comando("INSERT INTO Funcionarios ...", valores)
   except mysql.connector.Error as e:
       messagebox.showerror("Erro no Banco", f"Falha ao salvar: {e}")
   ```  

---

### **Exercício 3: Classe Gerenciadora de Janelas**  
**Objetivo:** Criar `GerenciadorJanelas` para trocar telas dinamicamente.  
**Tarefas:**  
1. A classe deve:  
   - Receber a janela raiz do Tkinter.  
   - Armazenar frames (ex: `CadastroFuncionarios`, `ListagemContratos`) como atributos.  
   - Ter um método `mostrar_frame(nome_frame)` para alternar entre telas.  
2. Exemplo de uso:  
   ```python  
   class MainApp:
       def __init__(self, root):
           self.gerenciador = GerenciadorJanelas(root)
           self.gerenciador.adicionar_frame("MenuPrincipal", MenuPrincipalFrame)
           self.gerenciador.mostrar_frame("MenuPrincipal")
   ```  

---

### **Exercício 4: Classe de Formulários Dinâmicos (Herança)**  
**Objetivo:** Criar `FormularioBase` para reutilização de layouts.  
**Tarefas:**  
1. A classe deve:  
   - Receber campos dinâmicos (ex: `[{"label": "Nome", "tipo": "entry"}]`).  
   - Gerar automaticamente labels, entries, comboboxes e validação.  
   - Ter um método `validar()` abstrato para ser implementado nas subclasses.  
2. Exemplo de subclasse:  
   ```python  
   class FormularioFuncionario(FormularioBase):
       def __init__(self, master):
           campos = [
               {"label": "CPF", "tipo": "entry", "validacao": "cpf"},
               {"label": "Departamento", "tipo": "combobox", "opcoes": ["TI", "RH"]}
           ]
           super().__init__(master, campos)
   ```  

---

### **Exercício 5: Módulo CRUD de Funcionários (MVC)**  
**Objetivo:** Implementar cadastro, edição e exclusão de funcionários.  
**Tarefas:**  
1. Crie:  
   - **Model**: Classe `FuncionarioModel` usando `GerenciadorBancoDados`.  
   - **View**: `FuncionarioView` usando `FormularioBase`.  
   - **Controller**: `FuncionarioController` para intermediar Model e View.  
2. Funcionalidades obrigatórias:  
   - Busca por CPF.  
   - Atualização de status (ativo/inativo).  

---

### **Exercício 6: Módulo de Contratos com Herança**  
**Objetivo:** Implementar contratos com cálculo automático de multa.  
**Tarefas:**  
1. Crie classes:  
   - `ContratoCLT`: Calcula multa como 40% do salário.  
   - `ContratoPJ`: Multa fixa de 10% do salário.  
2. Integre ao formulário de contratos (use herança de `ContratoBase`).  

---

### **Exercício 7: Folha de Pagamento com Polimorfismo**  
**Objetivo:** Calcular salário líquido considerando descontos e benefícios.  
**Tarefas:**  
1. Crie uma classe `CalculadoraPagamento`:  
   - Método `calcular_salario(contrato, horas)` retorna salário bruto.  
   - Método `calcular_liquido(bruto, descontos, beneficios)`.  
2. Integre ao formulário de folha de pagamento.  

---

### **Exercício 8: Relatórios com Gráficos**  
**Objetivo:** Gerar PDF/gráficos de custos por departamento.  
**Tarefas:**  
1. Use `matplotlib` para gráfico de pizza com custos.  
2. Use `fpdf2` para gerar um relatório em PDF com dados do banco.  

---

### **Exercício 9: Sistema de Login e Permissões**  
**Objetivo:** Restringir acesso a funções por perfil (ex: RH, Financeiro).  
**Tarefas:**  
1. Adicione tabela `Usuarios`:  
   ```sql  
   CREATE TABLE Usuarios (
       id INT PRIMARY KEY AUTO_INCREMENT,
       usuario VARCHAR(50) UNIQUE,
       senha VARCHAR(100),
       perfil ENUM('admin', 'rh', 'financeiro')
   );
   ```  
2. Crie janela de login e redirecione conforme perfil.  

---

### **Exercício 10: Integração Final (Passo a Passo)**  
**Objetivo:** Unir todos os módulos em um sistema coeso.  
**Tarefas:**  
1. Crie uma classe `MainWindow` com:  
   - Menu principal usando `GerenciadorJanelas`.  
   - Controle de sessão (usuário logado).  
2. Exemplo de estrutura:  
   ```python  
   class MainWindow(tk.Tk):
       def __init__(self):
           super().__init__()
           self.geometry("1024x768")
           self.gerenciador = GerenciadorJanelas(self)
           self.gerenciador.adicionar_frame("Login", LoginFrame)
           self.gerenciador.mostrar_frame("Login")
   ```  
3. Garanta que:  
   - Os controllers compartilhem a mesma instância de `GerenciadorBancoDados`.  
   - As janelas atualizem dados em tempo real (ex: ao adicionar funcionário, a lista é atualizada).  

---

### **Exercício 11: Testes, Documentação e GitHub**  
**Objetivo:** Entregar o projeto versionado e documentado.  
**Tarefas:**  
1. Crie testes unitários para:  
   - Validação de CPF.  
   - Cálculo de salário líquido.  
2. Documente:  
   - Adicione docstrings em todas as classes/métodos.  
   - Escreva um `README.md` com:  
     - Como configurar o banco de dados.  
     - Como executar o sistema.  
     - Estrutura do projeto (MVC, pastas).  
3. Suba para o GitHub:  
   - Crie um repositório público.  
   - Adicione um `.gitignore` para Python e arquivos temporários.  
   - Faça commits organizados (ex: "feat: módulo de contratos").  
   - Envie o link no Classroom.  

---

### **Prompt de Ajuda para Alunos**  
```
Precisa de ajuda? Formate sua dúvida assim:  
"Exercício [Nº]: [Título].  
Erro: [Cole o erro aqui].  
Código relevante: [Descreva o trecho problemático].  
O que já tentei: [Liste as tentativas]."  
Responderei com soluções passo a passo!
```

---

### **Notas para os Alunos**  
1. **Organização do Código:**  
   - Separe em pastas: `models`, `views`, `controllers`, `utils`.  
   - Use `requirements.txt` para listar dependências (ex: `mysql-connector-python==8.0.33`).  

2. **Dica de Arquitetura:**  
   ```  
   gestao_pessoal/  
   ├── main.py  
   ├── models/  
   │   ├── funcionario_model.py  
   │   └── contrato_model.py  
   ├── views/  
   │   ├── formularios.py  
   │   └── relatorios.py  
   └── controllers/  
       ├── funcionario_controller.py  
       └── auth_controller.py  
   ```  

3. **Prazo e Dúvidas:**  
   - A lista deve ser concluída em 4 semanas.  
   - Dúvidas técnicas podem ser enviadas via Classroom ou discutidas no fórum.  

--- 

**Pronto para usar em sala!** 🚀
