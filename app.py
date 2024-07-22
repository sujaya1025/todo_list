from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Ensure the directory for the database exists and create the database if it doesn't
if not os.path.exists(os.path.join(os.getcwd(), 'db.sqlite')):
    db.create_all()

class Todo(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    done = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    todo_list = Todo.query.all()
    return render_template('index.html', todo_list=todo_list)

@app.route('/add',methods=['POST'])
def add():
    name = request.form.get("name")
    new_task = Todo(name=name,done=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/update/<int:todo_id>',methods=['POST'])
def update(todo_id):
    todo = Todo.query.get(todo_id)
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/delete/<int:todo_id>',methods=['POST'])
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

if __name__=='__main__':
    app.run(debug= True)





"""
app = Flask(__name__)
tasks = []

class Task:
    def __init__(self, name, completed=False):
        self.name = name
        self.completed = completed

@app.route('/')
def index():
    # Add index numbers to tasks for rendering
    indexed_tasks = [(idx, task) for idx, task in enumerate(tasks)]
    return render_template('index.html', tasks=indexed_tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    task_name = request.form['task']
    tasks.append(Task(task_name))
    return redirect(url_for('index'))

@app.route('/toggle_task/<int:task_index>')
def toggle_task(task_index):
    tasks[task_index].completed = not tasks[task_index].completed
    return '', 204  # No content response

if __name__ == '__main__':
    app.run(debug=True)
"""