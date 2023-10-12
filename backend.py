from flask import Flask, render_template, request
from sqlalchemy import create_engine


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/cadaluno")
def cadaluno():
    return render_template("cadaluno.html")


@app.route("/cadprof")
def cadprof():
    return render_template("cadprof.html")


@app.route("/selecionar")
def selecionar():
    linhas = select_data("Select * from cadastro_aluno")
    return linhas


@app.route("/selecionar_prof")
def selecionarprof():
    linhas = select_data("Select * from cadastro_prof")
    return linhas


@app.route("/cadastrar", methods=['POST', 'GET'])
def cadastrar():
    nome = request.form['nome']
    data = request.form['txtano']
    sexo = request.form['radsex']
    email = request.form['email']
    insert_data(f"""insert into cadastro_aluno (nome, datanasc, sexo, email)
                VALUES ('{nome}', '{data}', '{sexo}', '{email}')""")
    message = "Cadastro realizado com sucesso!"
    return render_template('cadaluno.html', message=message)


@app.route("/cadastroprof", methods=['POST', 'GET'])
def cadastroprof():
    profnome = request.form['nome']
    profdata = request.form['profano']
    profsexo = request.form['profsex']
    profemail = request.form['profemail']
    proftreino = request.form['tipotreino']
    insert_data(f"""insert into cadastro_prof (nome, datanasc, sexo, email,
                treino)
        VALUES ('{profnome}', '{profdata}', '{profsexo}', '{profemail}',
        '{proftreino}')""")
    message = "Cadastro realizado com sucesso!"
    return render_template('cadprof.html', message=message)


def select_data(query):
    connection = create_connection()
    result = connection.execute(query)
    resultado_final = ""
    for row in result:
        resultado_final = resultado_final + "<br>" + str(row)
    return resultado_final


def insert_data(query):
    connection = create_connection()
    connection.execute(query)


def create_connection():
    engine = create_engine(
        "mysql+mysqlconnector://root:toto3010@localhost/cadastroacad")
    connection = engine.connect()
    return connection


if __name__ == "__main__":
    app.run(debug=True)
