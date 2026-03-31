from flask import Flask, render_template, redirect, request
from markupsafe import escape
import sqlite3
import os

def connect_db():
    #in case if the file doesn't exists
    file = 'database'
    if not os.path.exists(file):
        os.makedirs(file)
    
    path_db = os.path.join('database', 'to_do.db')
    conn = sqlite3.connect(path_db)
    return conn

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS Checklists (
                       id integer PRIMARY KEY AUTOINCREMENT,
                       titulo TEXT NOT NULL
                   )
                   """)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS Metas(
                       id integer PRIMARY KEY AUTOINCREMENT,
                       conteudo TEXT NOT NULL
                       )
                   """)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS Tarefas_checklist(
                       id integer PRIMARY KEY AUTOINCREMENT,
                       checklist_id INTEGER,
                       conteudo TEXT NOT NULL,
                       concluido INTEGER DEFAULT 0,
                       FOREIGN KEY (checklist_id) REFERENCES Checklists(id) ON DELETE CASCADE   
                   ) 
                   """)
    conn.commit()
    conn.close()
create_table()


app = Flask(__name__)




@app.route('/')
def home():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo FROM Checklists")
    todos_os_checklists = cursor.fetchall()
    checklist_com_tarefas = []
    for checklist in todos_os_checklists:
        checklist_id = checklist[0]
        cursor.execute("SELECT conteudo FROM Tarefas_checklist WHERE checklist_id = ?", (checklist_id,))
        tarefas_da_checklist = cursor.fetchall()
        pacote ={
            'id': checklist[0],
            'titulo': checklist[1],
            'tarefas': tarefas_da_checklist
        }
        checklist_com_tarefas.append(pacote)
    conn.close()
    return render_template('index.html', checklists=checklist_com_tarefas)

@app.route('/create_checklist', methods=['POST'])
def create():
    titulo = request.form.get('titulo')
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Checklists (titulo) VALUES (?)", (titulo,))
    conn.commit()
    conn.close()
    return redirect('/')


@app.route('/add_task/<int:checklist_id>', methods=['POST'])
def add_task(checklist_id):
    task_text = request.form['task']
    if task_text.strip():
        conn = connect_db()
        cursor = conn.cursor()
        #insert the text in the column 'conteudo'
        cursor.execute("INSERT INTO Tarefas_checklist (checklist_id, conteudo) VALUES (?, ?)", (checklist_id, task_text,))
        conn.commit()
        conn.close()
    return redirect('/')

@app.route("/delete_task/<int:id>")
def delete_task(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Checklists WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

# --- SEÇÃO DE METAS ---

@app.route('/page_meta')
def page_meta():
    return render_template('meta.html', metas=metas)

@app.route('/create_meta')
def create_meta():
    new_meta = []
    metas.append(new_meta) # cria uma meta vazia
    return redirect('/page_meta')

@app.route('/add_task_meta/<int:meta_id>', methods=['POST'])
def add_task_meta(meta_id):
    task_text = request.form['task_meta']
    if task_text.strip() != "":
        metas[meta_id].append(task_text)

    return redirect('/page_meta')


@app.route('/delete_task_meta/<int:meta_id>/<int:task_meta_id>')
def delete_task_meta(meta_id, task_meta_id):
    metas[meta_id].pop(task_meta_id)

    return redirect('/page_meta')


if __name__ == "__main__":
    app.run(debug=True)