from flask import Flask, render_template, request, url_for, flash, g
from werkzeug.utils import redirect
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'tarefas_colaborativas_db'

mysql = MySQL(app)


@app.route('/')
def Login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    usuario = request.form.get('usuario')
    senha = request.form.get('senha')

    cur = mysql.connection.cursor()

    cur.execute("SELECT u.id, u.nome_completo FROM  usuario u WHERE nome_usuario=%s AND senha=%s",
                (usuario, senha))

    # data = cur.fetchall()
    row = cur.fetchone()

    if (row is None):
        flash("Credenciais Incorrectas!")
        return render_template('login.html')
    else:
        usuario_logado_id = str(row[0])
        # g.user = usuario_logado_id

        f = open("temp.txt", "w")
        f.write(usuario_logado_id)
        f.close()

        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT t.id, t.titulo, t.descricao, e.nome, e.id FROM tarefa t JOIN estado e ON " +
            "(t.id_estado = e.id) JOIN tarefa_usuario tu ON (t.id = tu.id_tarefa ) " +
            "JOIN usuario u ON (u.id = tu.id_usuario) WHERE tu.id_usuario = %s", usuario_logado_id)
        data = cur.fetchall()

        cur.execute("SELECT * FROM usuario WHERE id != %s", usuario_logado_id)
        users = cur.fetchall()
        cur.close()
        return render_template('index.html', tarefas=data, usuarios=users, usuario=usuario_logado_id)


@app.route('/tarefas')
def Index():
    f = open("temp.txt", "r")
    # print("Usuário logado:" + f.read())
    usuario_logado_id = f.read()
    f.close()

    # print("Usuário logado:" + g.user)
    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT t.id, t.titulo, t.descricao, e.nome, e.id FROM tarefa t JOIN estado e ON " +
        "(t.id_estado = e.id) JOIN tarefa_usuario tu ON (t.id = tu.id_tarefa ) " +
        "JOIN usuario u ON (u.id = tu.id_usuario) WHERE tu.id_usuario = %s", usuario_logado_id)
    data = cur.fetchall()

    cur.execute("SELECT * FROM usuario WHERE id != %s", usuario_logado_id)
    users = cur.fetchall()
    cur.close()
    return render_template('index.html', tarefas=data, usuarios=users, usuario=usuario_logado_id)


@app.route('/insert', methods=['POST'])
def insert():
    f = open("temp.txt", "r")
    # print("Usuário logado:" + f.read())
    usuario_logado_id = f.read()
    f.close()
    if request.method == "POST":
        flash("Tarefa criada com Sucesso!")
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        id_estado = 1
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tarefa (titulo, descricao, id_estado) VALUES (%s, %s, %s)",
                    (titulo, descricao, id_estado))
        mysql.connection.commit()
        cur.execute("SELECT max(id) FROM tarefa")
        last_tarefa_id = str(cur.fetchone()[0])  # Pega o último id inserido
        print("############################################")
        print("Last tarefa id : " + last_tarefa_id)

        cur.execute("INSERT INTO tarefa_usuario (id_tarefa, id_usuario) VALUES (%s, %s)",
                    (last_tarefa_id, usuario_logado_id))
        mysql.connection.commit()
        cur.close()
      #  print("############################################")
        # print("Last tarefa id : " + row)
        return redirect(url_for('Index'))


@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    flash("Tarefa removida com sucesso")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tarefa_usuario WHERE id_tarefa=%s", (id_data,))
    mysql.connection.commit()
    cur.execute("DELETE FROM tarefa WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))


@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        id_estado = request.form['id_estado']
        print("###############################")
        print("Valor da chave: "+id_data)
        print("Valor do título: "+titulo)
        print("Valor da descrição: "+descricao)
        print("###############################")
        cur = mysql.connection.cursor()
        cur.execute("UPDATE tarefa SET titulo=%s, descricao=%s, id_estado=%s WHERE id=%s",
                    (titulo, descricao, id_estado, id_data))
        mysql.connection.commit()
        flash("Tarefa actualizada com sucesso")
        return redirect(url_for('Index'))


@app.route('/partilhar', methods=['POST', 'GET'])
def partilhar():
    flash("Tarefa partilhada com Sucesso!")
    if request.method == 'POST':
        id_usuario = request.form['id_usuario']
        id_tarefa = request.form['id_tarefa']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tarefa_usuario (id_tarefa, id_usuario) VALUES (%s, %s)",
                    (id_tarefa, id_usuario))
        mysql.connection.commit()

        return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)
