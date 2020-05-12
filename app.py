"""
------------------------------- Imports --------------------------------
"""
import os

from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from forms import AddTodo


"""
------------------------------- App Setup ------------------------------
"""
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12).hex()


"""
--------------------------- DB Setup & Migrate -------------------------
"""
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)


"""
-------------------------------- Models -------------------------------
"""
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    done = db.Column(db.Boolean, nullable=False)
    completed_on = db.Column(db.DateTime, nullable=True)

    def __init__(self, task, done):
        self.task = task
        self.done = done

    def __repr__(self):
        return self.task


"""
-------------------------------- Views --------------------------------
"""
@app.route('/', methods=['GET', 'POST'])
def todo():
    form = AddTodo()

    if request.method == 'POST':
        if form.validate_on_submit():
            item = Todo(task=form.item.data, done=False)
            db.session.add(item)
            db.session.commit()

            return redirect(url_for('todo'))
    else:
        items = Todo.query.filter_by(done=False).all()
        return render_template('todo.html', form=form, items=items)


@app.route('/edit/<int:pk>', methods=['POST'])
def edit(pk):
    if request.method == 'POST':
        item = Todo.query.get(pk)
        item.task = request.form['task']
        item.description = request.form['description']
        db.session.commit()

    return redirect(url_for('todo'))


@app.route('/done/<int:pk>')
def done(pk):
    item = Todo.query.get(pk)
    item.done = True
    item.completed_on = datetime.now()
    db.session.commit()

    return redirect(url_for('todo'))


@app.route('/delete/<int:pk>')
def delete(pk):
    item = Todo.query.get(pk)
    db.session.delete(item)
    db.session.commit()

    return redirect(url_for('todo'))


@app.route('/completed')
def completed():
    items = Todo.query.filter_by(done=True).all()
    return render_template('completed.html', items=items)


@app.route('/undone/<int:pk>')
def undone(pk):
    item = Todo.query.get(pk)
    item.done = False
    item.completed_on = None
    db.session.commit()

    return redirect(url_for('completed'))


"""
-------------------------------- Run App -------------------------------
"""
if __name__ == '__main__':
    app.run(debug=True)