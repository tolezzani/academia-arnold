from flask import Flask, render_template, request, url_for
from sqlalchemy import create_engine


app = Flask(__name__)


@app.route("/")
def base():

    return render_template("base.html")


@app.route("/contatos")
def contatos():
    return render_template("contatos.html")


@app.route("/selecionar")
def selecionar():
    linhas = select_data("Select * from cadastro")
    return linhas


@app.route("/cadastrar", methods=['POST', 'GET'])
def cadastrar():
    nome = request.form['nome']
    data = request.form['txtano']
    sexo = request.form['radsex']
    email = request.form['email']
    insert_data(f"""insert into cadastro (nome, datanasc, sexo, email)
                VALUES ('{nome}', '{data}', '{sexo}', '{email}')""")
    message = "Cadastro realizado com sucesso!"
    return render_template('base.html', message=message)


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
