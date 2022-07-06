from flask import Flask, redirect, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    contact=db.Column(db.String(20),nullable=False)
    collegename=db.Column(db.String(500),nullable=False)
    collegeaddress=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) ->str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET','POST'])
def hello():
    if request.method=='POST':
        title= request.form['title']
        desc = request.form['desc']
        contact = request.form['contact']
        collegename = request.form['collegename']
        collegeaddress = request.form['collegeaddress']
        todo=Todo(title=title,desc=desc,contact=contact,collegename=collegename,collegeaddress=collegeaddress)
        db.session.add(todo)
        db.session.commit()
    allTodo=Todo.query.all()
    
    return render_template('index.html', allTodo=allTodo)

@app.route('/database')
def products():
    allTodo=Todo.query.all()
    
    return render_template('database.html', allTodo=allTodo)

@app.route('/update/<int:sno>', methods=['GET','POST'])
def Update(sno):
    if request.method=='POST':
        title= request.form['title']
        desc = request.form['desc']
        contact = request.form['contact']
        collegename = request.form['collegename']
        collegeaddress = request.form['collegeaddress']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        todo.contact=contact
        todo.collegename=collegename
        todo.collegeaddress=collegeaddress
        db.session.add(todo)
        db.session.commit()
        return redirect("/database")

    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo) 

@app.route('/delete/<int:sno>')
def Delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/database')

if __name__ == "__main__":
    app.run(debug=True, port=8000)