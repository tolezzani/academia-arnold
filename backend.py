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
    matricula = request.form['matricula']
    treino = request.form['treino']
    if treino == "musculacao":
        profmus = selecionar_professor(treino="musculacao")
        horario = selecionar_horario(treino="musculacao")
        message = (
            f"{matricula} se matriculou em Musculação com o professor {profmus} nos dias segunda, quarta e sexta no período da {horario}.")
        insert_data(f"""insert into marque_treino (matricula, treino, professor)
        VALUES ("{matricula}", "{treino}", "{profmus}")""")
    elif treino == "natacao":
        profnat = selecionar_professor(treino="natacao")
        horario = selecionar_horario(treino="natacao")
        message = (
            f"{matricula} se matriculou em Natação com a professora {profnat} nos dias terça, quinta e sábado no período {horario}.")
        insert_data(f"""insert into marque_treino (matricula, treino, professor)
        VALUES ("{matricula}", "{treino}", "{profnat}")""")
    elif treino == "ioga":
        profioga = selecionar_professor(treino="ioga")
        horario = selecionar_horario(treino="ioga")
        message = (
            f"{matricula} se matriculou em Ioga com o professor {profioga} nos dias segunda, quarta e sexta no periodo da {horario}.")
        insert_data(f"""insert into marque_treino (matricula, treino, professor)
        VALUES ("{matricula}", "{treino}", "{profioga}")""")
    else:
        profcross = selecionar_professor(treino="crossfit")
        horario = selecionar_horario(treino="crossfit")
        message = (
            f"{matricula} se matriculou em Crossfit com a professora {profcross} nos dias terça, quinta e sábado no periodo da {horario}.")
        insert_data(f"""insert into marque_treino (matricula, treino, professor)
        VALUES ("{matricula}", "{treino}", "{profcross}")""")
    alunos = select_data("Select nome from cadastro_aluno")
    alunos = [aluno[0] for aluno in alunos]
    resultado_cadastro_treino = select_data(
        "Select treino from cadastro_treino")
    treinos = [treino[0] for treino in resultado_cadastro_treino]
    return render_template('cadmatri.html', message=message, name=alunos, treinos=treinos)


def selecionar_professor(treino):
    results = select_data(
        f"Select nome from cadastro_prof where treino = '{treino}'")
    for result in results:
        prof = result[0]
    return prof


def selecionar_horario(treino):
    results = select_data(
        f"Select horario from cadastro_treino where treino ='{treino}'")
    for result in results:
        hora = result[0]
    return hora


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
