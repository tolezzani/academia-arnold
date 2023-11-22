from flask import Flask, render_template, request, jsonify, url_for
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


@app.route("/cadtreino")
def cadtreino():
    return render_template("cadtreino.html")


@app.route("/cadmatri")
def cadmatri():
    alunos = select_data("Select nome from cadastro_aluno")
    alunos = [aluno[0] for aluno in alunos]
    resultado_cadastro_treino = select_data(
        "Select treino from cadastro_treino")
    treinos = [treino[0] for treino in resultado_cadastro_treino]
    # horarios = [treino[1] for treino in resultado_cadastro_treino]
    return render_template("cadmatri.html", name=alunos, treinos=treinos)


@app.route("/selecionar")
def selecionar():
    linhas = select_data("Select * from cadastro_aluno")
    return jsonify({'result': [dict(linha) for linha in linhas]})


@app.route("/selecionar_prof")
def selecionarprof():
    linhas = select_data("Select * from cadastro_prof")
    return jsonify({'result': [dict(linha) for linha in linhas]})


@app.route("/selecionar_treino")
def selecionartreino():
    linhas = select_data("Select * from cadastro_treino")
    return jsonify({'result': [dict(linha) for linha in linhas]})


@app.route("/selecionar_marque")
def selecionarmarque():
    linhas = select_data("Select * from marque_treino")
    return jsonify({'result': [dict(linha) for linha in linhas]})


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


@app.route("/cadastrotreino", methods=['POST', 'GET'])
def cadastrotreino():
    treino = request.form['tipotreino']
    dia_semana = request.form['dias_semana']
    horario = request.form['horario']
    insert_data(f"""insert into cadastro_treino (treino, dia_semana, horario)
        VALUES ('{treino}', '{dia_semana}', '{horario}')""")
    message = "Cadastro realizado com sucesso!"
    return render_template('cadtreino.html', message=message)


@app.route("/cadastromatri", methods=['POST', 'GET'])
def cadastromatri():
    professor = ""
    horario = ""
    matricula = request.form['matricula']
    treino = request.form['treino']
    profmus = select_data(
        "Select nome from cadastro_prof where treino = 'musculacao'")

    profnat = select_data(
        "Select nome from cadastro_prof where treino = 'natacao'")

    profioga = select_data(
        "Select nome from cadastro_prof where treino = 'ioga'")

    profcross = select_data(
        "Select nome from cadastro_prof where treino = 'crossfit'")

    if treino == "musculacao":
        for prof in profmus:
            professor = prof["nome"]
        periodo = select_data(
            "Select horario from cadastro_treino where treino = 'musculacao'")
        for hora in periodo:
            horario = hora["horario"]
        message = (
            f"{matricula} se matriculou em Musculação com o professor {professor} nos dias segunda, quarta e sexta no período da {horario}")
        insert_data(f"""insert into marque_treino (matricula, treino, professor)
        VALUES ("{matricula}", "{treino}", "{profmus}")""")
    elif treino == "natacao":
        for prof in profnat:
            professor = prof["nome"]
        periodo = select_data(
            "Select horario from cadastro_treino where treino = 'natacao'")
        for hora in periodo:
            horario = hora["horario"]
        message = (
            f"{matricula} se matriculou em Natação com o professor {professor} nos dias terça, quinta e sábado no período {horario}")
        insert_data(f"""insert into marque_treino (matricula, treino, professor)
        VALUES ("{matricula}", "{treino}", "{profnat}")""")
    elif treino == "ioga":
        for prof in profioga:
            professor = prof["nome"]
        periodo = select_data(
            "Select horario from cadastro_treino where treino = 'ioga'")
        for hora in periodo:
            horario = hora["horario"]
        message = (
            f"{matricula} se matriculou em Ioga com o professor {professor} nos dias segunda, quarta e sexta no periodo da {horario}")
        insert_data(f"""insert into marque_treino (matricula, treino, professor)
        VALUES ("{matricula}", "{treino}", "{profioga}")""")
    else:
        for prof in profcross:
            professor = prof["nome"]
        periodo = select_data(
            "Select horario from cadastro_treino where treino = 'crossfit'")
        for hora in periodo:
            horario = hora["horario"]
        message = (
            f"{matricula} se matriculou em Crossfit com o professor {professor} nos dias terça, quinta e sábado no periodo da {horario}")
        insert_data(f"""insert into marque_treino (matricula, treino, professor)
        VALUES ("{matricula}", "{treino}", "{profcross}")""")
    return render_template('cadmatri.html', message=message)


def select_data(query):
    connection = create_connection()
    result = connection.execute(query)
    resultado_final = []
    for row in result:
        resultado_final.append(row)
        # resultado_final = resultado_final + "<br>" + str(row)
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
