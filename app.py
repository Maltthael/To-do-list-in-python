from flask import Flask, render_template, redirect, request
from markupsafe import escape




app = Flask(__name__)

# Listas globais para armazenar os dados
checklists = []
metas = []

@app.route('/')
def home():
    return render_template('index.html', checklists=checklists)

@app.route('/create_checklist')
def create():
    new_checklist = []
    checklists.append(new_checklist) # cria uma checklist vazia

    return redirect('/')

@app.route('/add_task/<int:list_id>', methods=['POST'])
def add_task(list_id):
    task_text = request.form['task']
    if task_text.strip() != " ":
        checklists[list_id].append(task_text) # Adiciona uma tarefa dentro da checklist(Precisa ter um nome)

    return redirect('/')

@app.route("/delete_task/<int:list_id>/<int:task_id>")
def delete_task(list_id, task_id):
    checklists[list_id].pop(task_id)

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