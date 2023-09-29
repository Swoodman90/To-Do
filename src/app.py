from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') or 'sqlite:///myDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    todo_text = db.Column(db.String(100), index = True)

with app.app_context():
    db.create_all()

class ToDoForm(FlaskForm):
    todo = StringField("To-Do")
    submit = SubmitField("Add To-Do")


@app.route('/', methods=["GET", "POST"])
def index():
    
    if 'todo' in request.form:
        db.session.add(Todo(todo_text=request.form['todo']))
        db.session.commit()
    return render_template('index.html', todos=Todo.query.all(), template_form=ToDoForm())


@app.route('/remove_todo/<int:todo_id>')
def remove_todo(todo_id):
    todo_to_remove = Todo.query.get(todo_id)
    db.session.delete(todo_to_remove)
    db.session.commit()
    return redirect(url_for('index'))

