# Importa as bibliotecas necessárias
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Rota para a página inicial
@app.route('/')
def home():
    return render_template('index.html')

# Rota para listar os agendamentos
@app.route("/agendamentos")
def listar_agendamentos():
    conn = sqlite3.connect("petcare.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM agendamento ORDER BY data, horario")
    agendamentos = cursor.fetchall()
    conn.close()
    return render_template("agendamentos.html", agendamentos=agendamentos)

# Rota para cadastrar um novo agendamento
@app.route("/agendamentos/novo", methods=["GET", "POST"])
def novo_agendamento():
    if request.method == "POST":
        # Coleta os dados do formulário
        nome_cliente = request.form["nome_cliente"]
        nome_pet = request.form["nome_pet"]
        tipo_servico = request.form["tipo_servico"]
        data = request.form["data"]
        horario = request.form["horario"]
        observacoes = request.form["observacoes"]

        # Insere no banco de dados
        conn = sqlite3.connect("petcare.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO agendamento (nome_cliente, nome_pet, tipo_servico, data, horario, observacoes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nome_cliente, nome_pet, tipo_servico, data, horario, observacoes))
        conn.commit()
        conn.close()

        return redirect(url_for("listar_agendamentos"))
    
    return render_template("novo_agendamento.html")

# Rota para listar os clientes
@app.route("/clientes")
def listar_clientes():
    conn = sqlite3.connect("petcare.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cliente ORDER BY nome_cliente")
    clientes = cursor.fetchall()
    conn.close()
    return render_template("clientes.html", clientes=clientes)

# Rota para cadastrar um novo cliente
@app.route("/clientes/novo", methods=["GET", "POST"])
def novo_cliente():
    if request.method == "POST":
        nome_cliente = request.form["nome_cliente"]
        nome_pet = request.form["nome_pet"]
        telefone = request.form["telefone"]
        email = request.form["email"]
        endereco = request.form["endereco"]

        conn = sqlite3.connect("petcare.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO cliente (nome_cliente, nome_pet, telefone, email, endereco)
            VALUES (?, ?, ?, ?, ?)
        """, (nome_cliente, nome_pet, telefone, email, endereco))
        conn.commit()
        conn.close()

        return redirect(url_for("listar_clientes"))
    
    return render_template("novo_cliente.html")

# Função que cria as tabelas no banco se ainda não existirem
def init_db():
    conn = sqlite3.connect("petcare.db")
    cursor = conn.cursor()

    # Cria tabela de agendamentos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agendamento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_cliente TEXT NOT NULL,
            nome_pet TEXT NOT NULL,
            tipo_servico TEXT NOT NULL,
            data TEXT NOT NULL,
            horario TEXT NOT NULL,
            observacoes TEXT
        )
    ''')

    # Cria tabela de clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cliente (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_cliente TEXT NOT NULL,
            nome_pet TEXT NOT NULL,
            telefone TEXT,
            email TEXT,
            endereco TEXT
        )
    ''')

    # Cria tabela de pets
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pet (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_pet TEXT NOT NULL,
            nome_tutor TEXT NOT NULL,
            raca TEXT,
            idade INTEGER,
            peso REAL
        )
    ''')

    conn.commit()
    conn.close()

# Rota para editar um agendamento existente
@app.route("/agendamentos/editar/<int:id>", methods=["GET", "POST"])
def editar_agendamento(id):
    conn = sqlite3.connect("petcare.db")
    cursor = conn.cursor()

    if request.method == "POST":
        # Atualiza os dados do agendamento
        nome_cliente = request.form["nome_cliente"]
        nome_pet = request.form["nome_pet"]
        tipo_servico = request.form["tipo_servico"]
        data = request.form["data"]
        horario = request.form["horario"]
        observacoes = request.form["observacoes"]

        cursor.execute("""
            UPDATE agendamento
            SET nome_cliente=?, nome_pet=?, tipo_servico=?, data=?, horario=?, observacoes=?
            WHERE id=?
        """, (nome_cliente, nome_pet, tipo_servico, data, horario, observacoes, id))
        conn.commit()
        conn.close()
        return redirect(url_for("listar_agendamentos"))

    cursor.execute("SELECT * FROM agendamento WHERE id=?", (id,))
    agendamento = cursor.fetchone()
    conn.close()
    return render_template("editar_agendamento.html", agendamento=agendamento)

# Rota para excluir um agendamento
@app.route("/agendamentos/excluir/<int:id>")
def excluir_agendamento(id):
    conn = sqlite3.connect("petcare.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM agendamento WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("listar_agendamentos"))

# Rota para editar um cliente
@app.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):
    conn = sqlite3.connect("petcare.db")
    cursor = conn.cursor()

    if request.method == "POST":
        nome_cliente = request.form["nome_cliente"]
        nome_pet = request.form["nome_pet"]
        telefone = request.form["telefone"]
        email = request.form["email"]
        endereco = request.form["endereco"]

        cursor.execute("""
            UPDATE cliente
            SET nome_cliente = ?, nome_pet = ?, telefone = ?, email = ?, endereco = ?
            WHERE id = ?
        """, (nome_cliente, nome_pet, telefone, email, endereco, id))
        conn.commit()
        conn.close()
        return redirect(url_for("listar_clientes"))

    cursor.execute("SELECT * FROM cliente WHERE id = ?", (id,))
    cliente = cursor.fetchone()
    conn.close()
    return render_template("editar_cliente.html", cliente=cliente)

# Rota para excluir cliente
@app.route("/clientes/excluir/<int:id>")
def excluir_cliente(id):
    conn = sqlite3.connect("petcare.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cliente WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("listar_clientes"))

# Rota para listar pets
@app.route("/pets")
def listar_pets():
    conn = sqlite3.connect("petcare.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pet ORDER BY nome_pet")
    pets = cursor.fetchall()
    conn.close()
    return render_template("pets.html", pets=pets)

# Rota para cadastrar novo pet
@app.route("/pets/novo", methods=["GET", "POST"])
def novo_pet():
    if request.method == "POST":
        nome_pet = request.form["nome_pet"]
        nome_tutor = request.form["nome_tutor"]
        raca = request.form["raca"]
        idade = request.form["idade"]
        peso = request.form["peso"]

        conn = sqlite3.connect("petcare.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pet (nome_pet, nome_tutor, raca, idade, peso)
            VALUES (?, ?, ?, ?, ?)
        """, (nome_pet, nome_tutor, raca, idade, peso))
        conn.commit()
        conn.close()

        return redirect(url_for("listar_pets"))

    return render_template("novo_pet.html")

# Rota para editar pet
@app.route("/pets/editar/<int:id>", methods=["GET", "POST"])
def editar_pet(id):
    conn = sqlite3.connect("petcare.db")
    cursor = conn.cursor()

    if request.method == "POST":
        nome_pet = request.form["nome_pet"]
        nome_tutor = request.form["nome_tutor"]
        raca = request.form["raca"]
        idade = request.form["idade"]
        peso = request.form["peso"]

        cursor.execute("""
            UPDATE pet
            SET nome_pet = ?, nome_tutor = ?, raca = ?, idade = ?, peso = ?
            WHERE id = ?
        """, (nome_pet, nome_tutor, raca, idade, peso, id))
        conn.commit()
        conn.close()
        return redirect(url_for("listar_pets"))

    cursor.execute("SELECT * FROM pet WHERE id = ?", (id,))
    pet = cursor.fetchone()
    conn.close()
    return render_template("editar_pet.html", pet=pet)

# Rota para excluir pet
@app.route("/pets/excluir/<int:id>")
def excluir_pet(id):
    conn = sqlite3.connect("petcare.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pet WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("listar_pets"))

# Página de finanças: mostra total de clientes, pets, agendamentos e lucros
@app.route('/financas')
def financas():
    conn = sqlite3.connect("petcare.db")
    cursor = conn.cursor()

    # Totais
    cursor.execute("SELECT COUNT(*) FROM cliente")
    total_clientes = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM pet")
    total_pets = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM agendamento")
    total_agendamentos = cursor.fetchone()[0]

    # Dados para gráfico de tipos de serviço
    cursor.execute("SELECT tipo_servico, COUNT(*) FROM agendamento GROUP BY tipo_servico")
    dados = cursor.fetchall()
    tipos = [linha[0] for linha in dados]
    contagens = [linha[1] for linha in dados]

    # Tabela de preços
    precos = {
        'Banho': 40,
        'Tosa': 80,
        'Consulta': 100,
        'Vacinação': 70
    }

    # Lucro total (todos os agendamentos)
    cursor.execute("SELECT tipo_servico FROM agendamento")
    todos = cursor.fetchall()
    lucro_total = sum(precos.get(t[0], 0) for t in todos)

    # Lucro futuro (apenas agendamentos com data maior que hoje)
    from datetime import date
    hoje = date.today().isoformat()
    cursor.execute("SELECT tipo_servico FROM agendamento WHERE data > ?", (hoje,))
    futuros = cursor.fetchall()
    lucro_futuro = sum(precos.get(t[0], 0) for t in futuros)

    conn.close()

    return render_template("financas.html",
                           total_clientes=total_clientes,
                           total_pets=total_pets,
                           total_agendamentos=total_agendamentos,
                           tipos=tipos,
                           contagens=contagens,
                           lucro_total=lucro_total,
                           lucro_futuro=lucro_futuro)

# Inicia o servidor e cria as tabelas se não existirem
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
