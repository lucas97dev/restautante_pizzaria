import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os

# ---------- Funções principais ----------

# Cadastrar item no cardápio
def cadastrar_item_cardapio():
    def salvar_item():
        tipo = entry_tipo.get().strip()
        nome = entry_nome.get().strip()
        valor = entry_valor.get().strip()
        descricao = entry_descricao.get("1.0", tk.END).strip()

        if not tipo or not nome or not valor or not descricao:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        try:
            valor_float = float(valor)
        except ValueError:
            messagebox.showwarning("Erro", "Valor inválido. Use ponto para decimais (Ex: 19.99).")
            return

        arquivo_existe = os.path.exists("cardapio.csv")
        with open("cardapio.csv", "a", newline='', encoding='utf-8') as f:
            escritor = csv.writer(f)
            if not arquivo_existe:
                escritor.writerow(["tipo", "nome", "valor", "descricao"])
            escritor.writerow([tipo, nome, valor_float, descricao])

        messagebox.showinfo("Sucesso", f"Item cadastrado:\n{tipo} - {nome} - R${valor_float:.2f}")
        janela.destroy()

    janela = tk.Toplevel()
    janela.title("Cadastrar Item no Cardápio")

    tk.Label(janela, text="Tipo (Pizza, Porção, Marmitex, Almoço, Bebida):").pack()
    entry_tipo = tk.Entry(janela)
    entry_tipo.pack()

    tk.Label(janela, text="Nome do Produto:").pack()
    entry_nome = tk.Entry(janela)
    entry_nome.pack()

    tk.Label(janela, text="Valor (ex: 19.99):").pack()
    entry_valor = tk.Entry(janela)
    entry_valor.pack()

    tk.Label(janela, text="Descrição do Produto:").pack()
    entry_descricao = tk.Text(janela, height=4, width=40)
    entry_descricao.pack()

    tk.Button(janela, text="Salvar", command=salvar_item).pack(pady=10)

# Mostrar o cardápio
def mostrar_cardapio():
    if not os.path.exists("cardapio.csv"):
        messagebox.showinfo("Cardápio", "Nenhum item cadastrado no cardápio ainda.")
        return

    cardapio_por_tipo = {}

    with open("cardapio.csv", newline='', encoding='utf-8') as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            tipo = linha["tipo"].strip().capitalize()
            nome = linha["nome"]
            valor = float(linha["valor"])
            descricao = linha["descricao"]

            if tipo not in cardapio_por_tipo:
                cardapio_por_tipo[tipo] = []
            cardapio_por_tipo[tipo].append((nome, descricao, valor))

    janela = tk.Toplevel()
    janela.title("Cardápio Completo")

    canvas = tk.Canvas(janela)
    scrollbar = tk.Scrollbar(janela, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for tipo in sorted(cardapio_por_tipo.keys()):
        tk.Label(scroll_frame, text=tipo.upper(), font=("Arial", 14, "bold"), pady=5).pack()

        tabela = ttk.Treeview(scroll_frame, columns=("Nome", "Descricao", "Valor"), show="headings")
        tabela.heading("Nome", text="Nome")
        tabela.heading("Descricao", text="Descrição")
        tabela.heading("Valor", text="Valor (R$)")
        tabela.column("Nome", width=150)
        tabela.column("Descricao", width=700)
        tabela.column("Valor", width=200, anchor="center")

        for nome, descricao, valor in cardapio_por_tipo[tipo]:
            tabela.insert("", "end", values=(nome, descricao, f"R$ {valor:.2f}"))

        tabela.pack(pady=5)

# Excluir item do cardápio
def excluir_item():
    def confirmar_exclusao():
        nome = entry_nome.get()
        if not nome:
            messagebox.showwarning("Aviso", "Informe o nome do item a excluir.")
            return

        if not os.path.exists("cardapio.csv"):
            messagebox.showwarning("Erro", "O cardápio está vazio.")
            return

        atualizado = []
        removido = False
        with open("cardapio.csv", newline='', encoding='utf-8') as f:
            leitor = csv.DictReader(f)
            for linha in leitor:
                if linha["nome"].lower() != nome.lower():
                    atualizado.append(linha)
                else:
                    removido = True

        if removido:
            with open("cardapio.csv", "w", newline='', encoding='utf-8') as f:
                escritor = csv.DictWriter(f, fieldnames=["tipo", "nome", "valor", "descricao"])
                escritor.writeheader()
                escritor.writerows(atualizado)
            messagebox.showinfo("Sucesso", f"Item '{nome}' excluído do cardápio.")
        else:
            messagebox.showinfo("Info", f"Item '{nome}' não encontrado.")
        janela_exclusao.destroy()

    janela_exclusao = tk.Toplevel()
    janela_exclusao.title("Excluir Item do Cardápio")

    tk.Label(janela_exclusao, text="Nome do item a excluir:").pack()
    entry_nome = tk.Entry(janela_exclusao)
    entry_nome.pack()

    tk.Button(janela_exclusao, text="Excluir", command=confirmar_exclusao).pack(pady=10)

# Registrar venda
def registrar_venda():
    def salvar_venda():
        nome = entry_nome.get()
        quantidade = entry_quantidade.get()
        valor_total = entry_valor_total.get()

        if not nome or not quantidade or not valor_total:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        try:
            quantidade = int(quantidade)
            valor_total = float(valor_total)
        except ValueError:
            messagebox.showwarning("Erro", "Quantidade ou valor inválido.")
            return

        arquivo_existe = os.path.exists("vendas.csv")
        with open("vendas.csv", "a", newline='', encoding='utf-8') as f:
            escritor = csv.writer(f)
            if not arquivo_existe:
                escritor.writerow(["nome", "quantidade", "total"])
            escritor.writerow([nome, quantidade, valor_total])

        messagebox.showinfo("Sucesso", f"Venda registrada:\n{quantidade}x {nome} - R${valor_total:.2f}")
        janela_venda.destroy()

    janela_venda = tk.Toplevel()
    janela_venda.title("Registrar Venda")

    tk.Label(janela_venda, text="Nome do item vendido:").pack()
    entry_nome = tk.Entry(janela_venda)
    entry_nome.pack()

    tk.Label(janela_venda, text="Quantidade vendida:").pack()
    entry_quantidade = tk.Entry(janela_venda)
    entry_quantidade.pack()

    tk.Label(janela_venda, text="Valor total da venda:").pack()
    entry_valor_total = tk.Entry(janela_venda)
    entry_valor_total.pack()

    tk.Button(janela_venda, text="Registrar", command=salvar_venda).pack(pady=10)

# Ver relatório de vendas

import openpyxl

def ver_relatorio():
    if not os.path.exists("vendas.csv"):
        messagebox.showinfo("Relatório", "Nenhuma venda registrada ainda.")
        return

    vendas = []

    with open("vendas.csv", newline='', encoding='utf-8') as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            nome = linha["nome"]
            quantidade = int(linha["quantidade"])
            total = float(linha["total"])
            vendas.append((nome, quantidade, total))

    vendas.sort(key=lambda x: x[0].lower())

    janela = tk.Toplevel()
    janela.title("Relatório de Vendas")
    janela.geometry("650x650")

    canvas = tk.Canvas(janela)
    scrollbar = tk.Scrollbar(janela, orient="vertical", command=canvas.yview)
    frame_tabela = tk.Frame(canvas)

    frame_tabela.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=frame_tabela, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    tabela = ttk.Treeview(frame_tabela, columns=("Nome", "Quantidade", "Valor"), show="headings", height=25)
    tabela.heading("Nome", text="Nome")
    tabela.heading("Quantidade", text="Quantidade")
    tabela.heading("Valor", text="Valor Total (R$)")
    tabela.column("Nome", width=250)
    tabela.column("Quantidade", width=100, anchor="center")
    tabela.column("Valor", width=150, anchor="center")

    total_geral = 0

    for nome, qtd, total in vendas:
        tabela.insert("", "end", values=(nome, qtd, f"R$ {total:.2f}"))
        total_geral += total

    tabela.pack(pady=10)

    tk.Label(frame_tabela, text=f"Total Geral: R$ {total_geral:.2f}", font=("Arial", 12, "bold")).pack(pady=10)

    def exportar_excel():
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Relatório de Vendas"

        # Cabeçalhos
        ws.append(["Nome", "Quantidade", "Valor Total (R$)"])

        # Dados
        for nome, qtd, total in vendas:
            ws.append([nome, qtd, total])

        # Total Geral
        ws.append(["", "", f"Total: R$ {total_geral:.2f}"])

        # Salvar o arquivo
        nome_arquivo = "relatorio_vendas.xlsx"
        wb.save(nome_arquivo)

        messagebox.showinfo("Sucesso", f"Relatório exportado para '{nome_arquivo}' com sucesso!")

    # Botão para exportar
    tk.Button(frame_tabela, text="Exportar para Excel", command=exportar_excel).pack(pady=10)

def gerenciar_comanda_mesa():
    def abrir_comanda():
        numero = entry_mesa.get().strip()
        if not numero.isdigit():
            messagebox.showwarning("Erro", "Informe um número de mesa válido.")
            return
        janela_mesa.destroy()
        abrir_janela_comanda(int(numero))

    janela_mesa = tk.Toplevel()
    janela_mesa.title("Selecionar Mesa")
    tk.Label(janela_mesa, text="Número da mesa:").pack(pady=5)
    entry_mesa = tk.Entry(janela_mesa)
    entry_mesa.pack(pady=5)
    tk.Button(janela_mesa, text="Abrir Comanda", command=abrir_comanda).pack(pady=10)
    
def mostrar_comandas_ativas():
    janela = tk.Toplevel()
    janela.title("Comandas Ativas")
    janela.geometry("500x400")

    frame_tabela = tk.Frame(janela)
    frame_tabela.pack(fill="both", expand=True, padx=10, pady=10)

    tabela = ttk.Treeview(frame_tabela, columns=("Mesa", "Total"), show="headings")
    tabela.heading("Mesa", text="Mesa")
    tabela.heading("Total", text="Total (R$)")
    tabela.column("Mesa", width=100, anchor="center")
    tabela.column("Total", width=150, anchor="center")
    tabela.pack(fill="both", expand=True)

    comandas_encontradas = False

    for arquivo in os.listdir():
        if arquivo.startswith("comanda_mesa_") and arquivo.endswith(".csv"):
            try:
                mesa = arquivo.replace("comanda_mesa_", "").replace(".csv", "")
                total = 0
                with open(arquivo, newline='', encoding='utf-8') as f:
                    leitor = csv.DictReader(f)
                    for linha in leitor:
                        total += float(linha["total"])
                tabela.insert("", "end", values=(mesa, f"R$ {total:.2f}"))
                comandas_encontradas = True
            except Exception as e:
                print(f"Erro ao processar {arquivo}: {e}")

    if not comandas_encontradas:
        tk.Label(janela, text="Nenhuma comanda ativa encontrada.", font=("Arial", 12)).pack(pady=20)

    def abrir_comanda_selecionada():
        item = tabela.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione uma comanda para abrir.")
            return
        mesa = tabela.item(item)["values"][0]
        abrir_janela_comanda(int(mesa))

    def encerrar_comanda():
        item = tabela.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione uma comanda para encerrar.")
            return
        mesa = tabela.item(item)["values"][0]
        nome_arquivo = f"comanda_mesa_{mesa}.csv"

        if os.path.exists(nome_arquivo):
            try:
                # Transferir dados da comanda para o relatório de vendas
                with open(nome_arquivo, newline='', encoding='utf-8') as f:
                    leitor = csv.DictReader(f)
                    vendas = list(leitor)

                vendas_existe = os.path.exists("vendas.csv")
                with open("vendas.csv", "a", newline='', encoding='utf-8') as f:
                    campos = ["nome", "quantidade", "total"]
                    escritor = csv.DictWriter(f, fieldnames=campos)
                    if not vendas_existe:
                        escritor.writeheader()
                    for item in vendas:
                        escritor.writerow({
                            "nome": item["produto"],
                            "quantidade": item["quantidade"],
                            "total": item["total"]
                        })

                os.remove(nome_arquivo)
                messagebox.showinfo("Comanda Encerrada", f"Comanda da mesa {mesa} foi encerrada e enviada para o relatório de vendas.")
                janela.destroy()
                mostrar_comandas_ativas()

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao encerrar comanda: {e}")

    btn_frame = tk.Frame(janela)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Abrir Comanda Selecionada", command=abrir_comanda_selecionada).pack(side="left", padx=10)
    tk.Button(btn_frame, text="Encerrar Comanda", command=encerrar_comanda).pack(side="left", padx=10)
    

def abrir_janela_comanda(numero_mesa):
    nome_arquivo = f"comanda_mesa_{numero_mesa}.csv"

    janela = tk.Toplevel()
    janela.title(f"Comanda - Mesa {numero_mesa}")
    janela.geometry("500x450")

    def adicionar_item():
        produto = entry_produto.get().strip()
        quantidade = entry_quantidade.get().strip()
        valor = entry_valor.get().strip()

        if not produto or not quantidade or not valor:
            messagebox.showwarning("Erro", "Preencha todos os campos.")
            return

        try:
            qtd = int(quantidade)
            valor_unit = float(valor)
            total = qtd * valor_unit
        except ValueError:
            messagebox.showwarning("Erro", "Quantidade ou valor inválido.")
            return

        novo_item = {
            "produto": produto,
            "quantidade": qtd,
            "valor_unitario": valor_unit,
            "total": total
        }

        arquivo_existe = os.path.exists(nome_arquivo)
        with open(nome_arquivo, "a", newline='', encoding='utf-8') as f:
            escritor = csv.DictWriter(f, fieldnames=["produto", "quantidade", "valor_unitario", "total"])
            if not arquivo_existe:
                escritor.writeheader()
            escritor.writerow(novo_item)

        atualizar_lista()
        entry_produto.delete(0, tk.END)
        entry_quantidade.delete(0, tk.END)
        entry_valor.delete(0, tk.END)

    def atualizar_lista():
        for item in tabela.get_children():
            tabela.delete(item)

        total_comanda = 0
        if os.path.exists(nome_arquivo):
            with open(nome_arquivo, newline='', encoding='utf-8') as f:
                leitor = csv.DictReader(f)
                for linha in leitor:
                    tabela.insert("", "end", values=(
                        linha["produto"],
                        linha["quantidade"],
                        f"R$ {float(linha['valor_unitario']):.2f}",
                        f"R$ {float(linha['total']):.2f}"
                    ))
                    total_comanda += float(linha["total"])
        lbl_total.config(text=f"Total da Comanda: R$ {total_comanda:.2f}")

    # Campos
    frame_form = tk.Frame(janela)
    frame_form.pack(pady=10)

    tk.Label(frame_form, text="Produto:").grid(row=0, column=0, padx=5)
    entry_produto = tk.Entry(frame_form)
    entry_produto.grid(row=0, column=1)

    tk.Label(frame_form, text="Quantidade:").grid(row=1, column=0, padx=5)
    entry_quantidade = tk.Entry(frame_form)
    entry_quantidade.grid(row=1, column=1)

    tk.Label(frame_form, text="Valor Unitário:").grid(row=2, column=0, padx=5)
    entry_valor = tk.Entry(frame_form)
    entry_valor.grid(row=2, column=1)

    tk.Button(frame_form, text="Adicionar", command=adicionar_item).grid(row=3, columnspan=2, pady=10)

    # Tabela
    tabela = ttk.Treeview(janela, columns=("Produto", "Qtd", "Valor Unit.", "Total"), show="headings")
    tabela.heading("Produto", text="Produto")
    tabela.heading("Qtd", text="Qtd")
    tabela.heading("Valor Unit.", text="Valor Unit.")
    tabela.heading("Total", text="Total")
    tabela.pack(pady=10)

    lbl_total = tk.Label(janela, text="Total da Comanda: R$ 0.00", font=("Arial", 12, "bold"))
    lbl_total.pack(pady=5)

    atualizar_lista()

# Cadastrar ingrediente no estoque
def cadastrar_ingrediente():
    def salvar_ingrediente():
        nome = entry_nome.get().strip().title()
        quantidade = entry_quantidade.get().strip()
        unidade = entry_unidade.get().strip().lower()

        if not nome or not quantidade or not unidade:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        try:
            quantidade_float = float(quantidade)
        except ValueError:
            messagebox.showwarning("Aviso", "Quantidade inválida.")
            return

        novo_ingrediente = {
            "nome": nome,
            "quantidade": quantidade_float,
            "unidade": unidade
        }

        arquivo_existe = os.path.exists("estoque.csv")
        with open("estoque.csv", "a", newline='', encoding='utf-8') as f:
            escritor = csv.DictWriter(f, fieldnames=["nome", "quantidade", "unidade"])
            if not arquivo_existe:
                escritor.writeheader()
            escritor.writerow(novo_ingrediente)

        messagebox.showinfo("Sucesso", f"Ingrediente '{nome}' cadastrado no estoque.")
        janela_ingrediente.destroy()

    janela_ingrediente = tk.Toplevel()
    janela_ingrediente.title("Cadastrar Ingrediente no Estoque")
    janela_ingrediente.geometry("350x300")

    tk.Label(janela_ingrediente, text="Nome do ingrediente:").pack(pady=5)
    entry_nome = tk.Entry(janela_ingrediente, width=30)
    entry_nome.pack()

    tk.Label(janela_ingrediente, text="Quantidade disponível:").pack(pady=5)
    entry_quantidade = tk.Entry(janela_ingrediente, width=30)
    entry_quantidade.pack()

    tk.Label(janela_ingrediente, text="Unidade (ex: kg, g, L, ml, un):").pack(pady=5)
    entry_unidade = tk.Entry(janela_ingrediente, width=30)
    entry_unidade.pack()

    tk.Button(janela_ingrediente, text="Salvar", command=salvar_ingrediente).pack(pady=15)

# Registrar gasto
def registrar_gasto():
    def salvar_gasto():
        descricao = entry_descricao.get()
        valor = entry_valor.get()

        if not descricao or not valor:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        try:
            valor = float(valor)
        except ValueError:
            messagebox.showwarning("Aviso", "Valor inválido.")
            return

        arquivo_existe = os.path.exists("gastos.csv")
        with open("gastos.csv", "a", newline='', encoding='utf-8') as f:
            escritor = csv.writer(f)
            if not arquivo_existe:
                escritor.writerow(["descricao", "valor"])
            escritor.writerow([descricao, valor])

        messagebox.showinfo("Sucesso", f"Gasto registrado: {descricao} - R${valor:.2f}")
        janela_gasto.destroy()

    janela_gasto = tk.Toplevel()
    janela_gasto.title("Registrar Gasto")

    tk.Label(janela_gasto, text="Descrição do gasto:").pack()
    entry_descricao = tk.Entry(janela_gasto)
    entry_descricao.pack()

    tk.Label(janela_gasto, text="Valor:").pack()
    entry_valor = tk.Entry(janela_gasto)
    entry_valor.pack()

    tk.Button(janela_gasto, text="Salvar", command=salvar_gasto).pack(pady=10)

# ---------- Interface principal ----------

janela = tk.Tk()
janela.title("Restaurante e Pizzaria do Lúcio")
janela.geometry("420x500")

tk.Label(janela, text="Sistema de Gestão", font=("Arial", 16, "bold")).pack(pady=10)
tk.Label(janela, text="Restaurante e Pizzaria do Lúcio", font=("Arial", 16, "bold")).pack(pady=10)

tk.Button(janela, text="Cadastrar Item no Cardápio", command=cadastrar_item_cardapio, width=35).pack(pady=5)
tk.Button(janela, text="Mostrar Cardápio", command=mostrar_cardapio, width=35).pack(pady=5)
tk.Button(janela, text="Excluir Item do Cardápio", command=excluir_item, width=35).pack(pady=5)
tk.Button(janela, text="Registrar Venda", command=registrar_venda, width=35).pack(pady=5)
tk.Button(janela, text="Gerenciar Comandas por Mesa", command=gerenciar_comanda_mesa, width=35).pack(pady=5)
tk.Button(janela, text="Ver Comandas Ativas", width=35, command=mostrar_comandas_ativas).pack(pady=5)
tk.Button(janela, text="Ver Relatório de Vendas", command=ver_relatorio, width=35).pack(pady=5)
tk.Button(janela, text="Cadastrar Ingrediente no Estoque", command=cadastrar_ingrediente, width=35).pack(pady=5)
tk.Button(janela, text="Registrar Gasto", command=registrar_gasto, width=35).pack(pady=5)

janela.mainloop()
