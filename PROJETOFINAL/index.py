import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog

def create_db():
    conn = sqlite3.connect('meu_banco.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS pessoas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        email TEXT,
                        telefone TEXT,
                        endereco TEXT)''')
    conn.commit()
    conn.close()

def salvar():
    nome = entry_nome.get()
    email = entry_email.get()
    telefone = entry_telefone.get()
    endereco = entry_endereco.get()

    if nome:  
        conn = sqlite3.connect('meu_banco.db')
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO pessoas (nome, email, telefone, endereco) 
                          VALUES (?, ?, ?, ?)''', (nome, email, telefone, endereco))

        conn.commit()
        conn.close()

        messagebox.showinfo('CONFIRMADO', 'Cadastro realizado com sucesso')
        listar_nomes()
        limpar_campos()
    else:
        messagebox.showerror('Erro', 'O nome não pode ser vazio')

def listar_nomes():
    conn = sqlite3.connect('meu_banco.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pessoas")
    registros = cursor.fetchall()
    conn.close()

    listbox.delete(0, tk.END)
    for registro in registros:
        listbox.insert(tk.END, f"ID: {registro[0]}, Nome: {registro[1]}")

def deletar_item():
    conn = sqlite3.connect('meu_banco.db')
    cursor = conn.cursor()

    selecionado = listbox.curselection()

    if selecionado:
        item = listbox.get(selecionado)
        item_id = item.split(",")[0].split(":")[1].strip()

        cursor.execute("DELETE FROM pessoas WHERE id=?", (item_id,))
        conn.commit()
        listbox.delete(selecionado)

    conn.close()

def editar_item():
    selected_index = listbox.curselection()

    if selected_index:
        current_value = listbox.get(selected_index)
        item_id = current_value.split(",")[0].split(":")[1].strip()

        conn = sqlite3.connect('meu_banco.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nome, email, telefone, endereco FROM pessoas WHERE id=?", (item_id,))
        cliente = cursor.fetchone()  
        conn.close()

        if cliente:
            nome_atual, email_atual, telefone_atual, endereco_atual = cliente
            
            nome = simpledialog.askstring("Editar Item", "Digite o novo nome:", initialvalue=nome_atual)
            email = simpledialog.askstring("Editar Item", "Digite o novo email:", initialvalue=email_atual)
            telefone = simpledialog.askstring("Editar Item", "Digite o novo telefone:", initialvalue=telefone_atual)
            endereco = simpledialog.askstring("Editar Item", "Digite o novo endereço:", initialvalue=endereco_atual)

            if nome and email and telefone and endereco:
                conn = sqlite3.connect('meu_banco.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE pessoas SET nome=?, email=?, telefone=?, endereco=? WHERE id=?",
                               (nome, email, telefone, endereco, item_id))
                conn.commit()
                conn.close()

                listbox.delete(selected_index)
                listbox.insert(selected_index, f"ID: {item_id}, Nome: {nome}")

                messagebox.showinfo("Sucesso", "Item atualizado com sucesso!")
            else:
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
        else:
            messagebox.showerror("Erro", "Cliente não encontrado no banco de dados.")
    else:
        messagebox.showerror("Erro", "Nenhum item selecionado!")

def visualizar_cliente():
    try:
        selecionado = listbox.curselection()
        
        if not selecionado:
            raise ValueError("Nenhum item selecionado.")

        item_texto = listbox.get(selecionado) 
        item_id = item_texto.split(",")[0].split(":")[1].strip() 

        conn = sqlite3.connect('meu_banco.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nome, email, telefone, endereco FROM pessoas WHERE id=?", (item_id,))
        cliente = cursor.fetchone()  
        conn.close()

        if cliente:
            nome, email, telefone, endereco = cliente
            messagebox.showinfo("Informações do Cliente", f"Nome: {nome}\nEmail: {email}\nTelefone: {telefone}\nEndereço: {endereco}")
        else:
            messagebox.showerror("Erro", "Cliente não encontrado no banco de dados.")

    except Exception as e:
        messagebox.showerror("Erro", str(e))

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    entry_endereco.delete(0, tk.END)

root = tk.Tk()
root.title('Cadastro de pessoas')

tk.Label(root, text='Nome: ').grid(row=0, column=0, padx=10, pady=10)
entry_nome = tk.Entry(root)
entry_nome.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text='Email: ').grid(row=1, column=0, padx=10, pady=10)
entry_email = tk.Entry(root)
entry_email.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text='Telefone: ').grid(row=2, column=0, padx=10, pady=10)
entry_telefone = tk.Entry(root)
entry_telefone.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text='Endereço: ').grid(row=3, column=0, padx=10, pady=10)
entry_endereco = tk.Entry(root)
entry_endereco.grid(row=3, column=1, padx=10, pady=10)

btn_salvar = tk.Button(root, text='Salvar', command=salvar)
btn_salvar.grid(row=4, column=0, columnspan=2, pady=10)

btn_deletar = tk.Button(root, text='Excluir usuario', command=deletar_item)
btn_deletar.grid(row=5, column=0, columnspan=2, pady=10)

btn_editar = tk.Button(root, text='Editar', command=editar_item)
btn_editar.grid(row=6, column=0, columnspan=2, pady=10)

btn_visualizar = tk.Button(root, text='Visualizar', command=visualizar_cliente)
btn_visualizar.grid(row=8, column=0, columnspan=2, pady=10)

listbox = tk.Listbox(root, width=40, height=10)
listbox.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

create_db()
listar_nomes()

root.mainloop()
