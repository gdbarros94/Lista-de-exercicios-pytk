import tkinter as tk

class GerenciadorJanelas:
    def __init__(self, root):
        self.root = root
        self.frames = {}
        self.frame_atual = None
        
        # Criar container principal
        self.container = tk.Frame(self.root)
        self.container.pack(side="top", fill="both", expand=True)
        
    def adicionar_frame(self, nome, frame):
        """Adiciona um frame ao gerenciador"""
        self.frames[nome] = frame
        frame.grid(row=0, column=0, sticky="nsew", in_=self.container)
        frame.grid_remove()  # Esconde o frame inicialmente
        
    def mostrar_frame(self, nome):
        """Mostra o frame especificado e esconde o atual"""
        if self.frame_atual:
            self.frame_atual.grid_remove()
        
        frame = self.frames.get(nome)
        if frame:
            frame.grid()
            self.frame_atual = frame
        else:
            raise ValueError(f"Frame '{nome}' não encontrado") 