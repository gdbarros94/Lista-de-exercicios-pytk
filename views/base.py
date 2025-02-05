import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod

class FormularioBase(tk.Frame, ABC):
    def __init__(self, master, campos):
        super().__init__(master)
        self.campos = campos
        self.widgets = {}
        self.criar_formulario()
        
    def criar_formulario(self):
        for i, campo in enumerate(self.campos):
            label = tk.Label(self, text=campo["label"])
            label.grid(row=i, column=0, padx=5, pady=5)
            
            if campo["tipo"] == "entry":
                widget = ttk.Entry(self)
                widget.grid(row=i, column=1, padx=5, pady=5)
            elif campo["tipo"] == "combobox":
                widget = ttk.Combobox(self, values=campo.get("opcoes", []))
                widget.grid(row=i, column=1, padx=5, pady=5)
                
            self.widgets[campo["label"]] = widget
            
    @abstractmethod
    def validar(self):
        pass
        
    def obter_dados(self):
        return {campo["label"]: self.widgets[campo["label"]].get() 
                for campo in self.campos} 