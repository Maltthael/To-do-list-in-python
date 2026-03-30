from flask import Flask, render_template, redirect, request
from markupsafe import escape


app = Flask(__name__)

checklists = []
metas = []

@app.route('/')
def home():
    return render_template('index.html', checklists = checklists)

@app.route('/create_checklist')
def create():
    new_checklist = []
    checklists.append(new_checklist) #create a empty checklist
    return redirect('/')

@app.route('/add_task/<int:list_id>', methods = ['POST'])
def add_task(list_id):
    task_text = request.form['task']
    if task_text.strip() != " ":
        checklists[list_id].append(task_text) # Adiciona uma tarefa dentro da checklist(Precisa ter um nome)
    return redirect('/')


@app.route("/delete_task/<int:list_id>/<int:task_id>")
def delete_task(list_id, task_id):
    checklists[list_id].pop(task_id)
    return redirect("/")


@app.route('/meta')
def page_meta():
    return render_template('meta.html', metas = metas)


@app.route('/create_meta')
def create_m():
    new_meta = []
    metas.append(new_meta) #create an empty meta
    return redirect('/meta')


@app.route('/add_task_meta/<int:list_meta_id>', methods = ['POST'])
def add_task_meta(list_meta_id):
    task_text = request.form['task_meta']
    if task_text.strip() != " ":
        metas[list_meta_id].append(task_text)
    return redirect('/meta')


if __name__ == "__main__":
    app.run(debug=True)