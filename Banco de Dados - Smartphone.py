import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# Função para carregar dados do arquivo JSON
def carregar_dados():
    if os.path.exists('smartphones.json'):
        with open('smartphones.json', 'r') as f:
            return json.load(f)
    return []

# Função para salvar dados no arquivo JSON
def salvar_dados(dados):
    with open('smartphones.json', 'w') as f:
        json.dump(dados, f, indent=4)

# Função para cadastrar um novo smartphone
def cadastrar_smartphone():
    codigo = entry_codigo.get()
    fabricante = combo_fabricante.get()
    velocidade = entry_velocidade.get()
    nucleos = combo_nucleos.get()
    armazenamento = entry_armazenamento.get()

    if not (codigo and fabricante and velocidade and nucleos and armazenamento):
        messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
        return

    smartphone = {
        "codigo": codigo,
        "fabricante": fabricante,
        "velocidade": velocidade,
        "nucleos": nucleos,
        "armazenamento": armazenamento
    }
    smartphones.append(smartphone)
    salvar_dados(smartphones)
    atualizar_tabela()
    messagebox.showinfo("Sucesso", "Smartphone cadastrado com sucesso!")
    limpar_campos()

# Função para limpar os campos de entrada
def limpar_campos():
    entry_codigo.delete(0, tk.END)
    combo_fabricante.set("")
    entry_velocidade.delete(0, tk.END)
    combo_nucleos.set("")
    entry_armazenamento.delete(0, tk.END)
    botao_salvar.config(state=tk.DISABLED)  # Desativa o botão de salvar

# Função para atualizar a tabela de smartphones
def atualizar_tabela():
    for row in tree.get_children():
        tree.delete(row)
    for idx, smartphone in enumerate(smartphones):
        tree.insert("", "end", iid=idx, values=(
            smartphone["codigo"],
            smartphone["fabricante"],
            smartphone["velocidade"],
            smartphone["nucleos"],
            smartphone["armazenamento"]
        ))

# Função para editar um smartphone
def editar_smartphone():
    item_selecionado = tree.focus()
    if not item_selecionado:
        messagebox.showwarning("Atenção", "Selecione um smartphone para editar.")
        return

    idx = int(item_selecionado)
    smartphone = smartphones[idx]
    
    entry_codigo.delete(0, tk.END)
    entry_codigo.insert(0, smartphone["codigo"])
    
    combo_fabricante.set(smartphone["fabricante"])
    entry_velocidade.delete(0, tk.END)
    entry_velocidade.insert(0, smartphone["velocidade"])
    
    combo_nucleos.set(smartphone["nucleos"])
    entry_armazenamento.delete(0, tk.END)
    entry_armazenamento.insert(0, smartphone["armazenamento"])

    botao_salvar.config(state=tk.NORMAL)  # Habilita o botão de salvar

# Função para salvar as alterações de um smartphone
def salvar_alteracoes():
    item_selecionado = tree.focus()
    if not item_selecionado:
        messagebox.showwarning("Atenção", "Selecione um smartphone para salvar as alterações.")
        return

    idx = int(item_selecionado)
    smartphones[idx]["codigo"] = entry_codigo.get()
    smartphones[idx]["fabricante"] = combo_fabricante.get()
    smartphones[idx]["velocidade"] = entry_velocidade.get()
    smartphones[idx]["nucleos"] = combo_nucleos.get()
    smartphones[idx]["armazenamento"] = entry_armazenamento.get()

    salvar_dados(smartphones)
    atualizar_tabela()
    messagebox.showinfo("Sucesso", "Alterações salvas com sucesso!")
    limpar_campos()

# Função para excluir um smartphone
def excluir_smartphone():
    item_selecionado = tree.focus()
    if not item_selecionado:
        messagebox.showwarning("Atenção", "Selecione um smartphone para excluir.")
        return

    idx = int(item_selecionado)
    del smartphones[idx]
    salvar_dados(smartphones)
    atualizar_tabela()
    messagebox.showinfo("Sucesso", "Smartphone excluído com sucesso!")
    limpar_campos()

# Função para buscar smartphones pelo código
def buscar_smartphone():
    fabricante_busca = entry_busca.get().strip()
    if fabricante_busca:
        resultado_busca = [smartphone for smartphone in smartphones if fabricante_busca.lower() in smartphone["fabricante"].lower()]
    else:
        resultado_busca = smartphones

    # Atualiza a tabela com os resultados da busca
    for row in tree.get_children():
        tree.delete(row)
    for idx, smartphone in enumerate(resultado_busca):
        tree.insert("", "end", iid=idx, values=(
            smartphone["codigo"],
            smartphone["fabricante"],
            smartphone["velocidade"],
            smartphone["nucleos"],
            smartphone["armazenamento"]
        ))

# Configurações da janela principal
root = tk.Tk()
root.title("Cadastro de Smartphones")
root.geometry("800x500")
root.config(bg="#f0f0f0")

# Carregar dados dos smartphones
smartphones = carregar_dados()

# Frame de Cadastro
frame_cadastro = tk.Frame(root, bg="#ffffff", padx=20, pady=20)
frame_cadastro.pack(side=tk.TOP, fill=tk.X)

tk.Label(frame_cadastro, text="Código do Smartphone:", bg="#ffffff").grid(row=0, column=0, padx=5, pady=5)
entry_codigo = tk.Entry(frame_cadastro)
entry_codigo.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_cadastro, text="Fabricante:", bg="#ffffff").grid(row=1, column=0, padx=5, pady=5)
combo_fabricante = ttk.Combobox(frame_cadastro, values=[
    "Samsung", "Motorola", "Apple", "Nokia", "Sony", "Google", "Microsoft", "Xiaomi", "One Plus", "Huawei"
])
combo_fabricante.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_cadastro, text="Velocidade do Processador (GHz):", bg="#ffffff").grid(row=2, column=0, padx=5, pady=5)
entry_velocidade = tk.Entry(frame_cadastro)
entry_velocidade.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_cadastro, text="Núcleos do Processador:", bg="#ffffff").grid(row=3, column=0, padx=5, pady=5)
combo_nucleos = ttk.Combobox(frame_cadastro, values=["8", "10", "12", "16"])
combo_nucleos.grid(row=3, column=1, padx=5, pady=5)

tk.Label(frame_cadastro, text="Armazenamento Interno (GB):", bg="#ffffff").grid(row=4, column=0, padx=5, pady=5)
entry_armazenamento = tk.Entry(frame_cadastro)
entry_armazenamento.grid(row=4, column=1, padx=5, pady=5)

# Botões
tk.Button(frame_cadastro, text="Cadastrar Smartphone", bg="#007BFF", fg="white", command=cadastrar_smartphone).grid(row=5, column=0, columnspan=1, pady=10)
tk.Button(frame_cadastro, text="Editar Smartphone", bg="#28a745", fg="white", command=editar_smartphone).grid(row=5, column=1, pady=10)
tk.Button(frame_cadastro, text="Salvar Alterações", bg="#ffc107", fg="black", command=salvar_alteracoes).grid(row=5, column=2, pady=10)
tk.Button(frame_cadastro, text="Excluir Smartphone", bg="#dc3545", fg="white", command=excluir_smartphone).grid(row=5, column=3, pady=10)

# Frame de Busca
frame_busca = tk.Frame(root, bg="#f0f0f0", padx=20, pady=10)
frame_busca.pack(side=tk.TOP, fill=tk.X)

tk.Label(frame_busca, text="Buscar pelo Nome do Smartphone:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5, pady=5)
entry_busca = tk.Entry(frame_busca)
entry_busca.pack(side=tk.LEFT, padx=5, pady=5)

# Botão de Busca
tk.Button(frame_busca, text="Buscar", bg="#007BFF", fg="white", command=buscar_smartphone).pack(side=tk.LEFT, padx=5, pady=5)

# Frame de Tabela com Scrollbar
frame_tabela = tk.Frame(root, bg="#f0f0f0", padx=20, pady=10)
frame_tabela.pack(fill=tk.BOTH, expand=True)

# Barra de rolagem vertical
scrollbar = tk.Scrollbar(frame_tabela)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Tabela de visualização dos smartphones
tree = ttk.Treeview(frame_tabela, columns=("codigo", "fabricante", "velocidade", "nucleos", "armazenamento"), show="headings", yscrollcommand=scrollbar.set)
tree.heading("codigo", text="Código")
tree.heading("fabricante", text="Fabricante")
tree.heading("velocidade", text="Velocidade (GHz)")
tree.heading("nucleos", text="Núcleos")
tree.heading("armazenamento", text="Armazenamento (GB)")
tree.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=tree.yview)

# Inicializa a tabela
atualizar_tabela()

# Desativa o botão de salvar inicialmente
botao_salvar = tk.Button(frame_cadastro, text="Salvar Alterações", bg="#ffc107", fg="black", command=salvar_alteracoes)
botao_salvar.grid(row=5, column=2, pady=10)
botao_salvar.config(state=tk.DISABLED)  # Desativa o botão de salvar

root.mainloop()
