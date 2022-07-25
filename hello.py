from email.policy import default
from flask import Flask, redirect, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    push=db.Column(db.Integer,nullable=False)
    pull=db.Column(db.Integer,nullable=False)
    legs=db.Column(db.Integer,nullable=False)
    abs=db.Column(db.Integer,nullable=False)
    cardio=db.Column(db.Integer,nullable=False)
    protien=db.Column(db.Integer,nullable=False)
    date=db.Column(db.String(11),nullable=False)

    def __repr__(self) ->str:
        return f"{self.sno} - {self.push}"

@app.route('/', methods=['GET','POST'])
def hello():
    if request.method=='POST':
        push= request.form['push']
        pull = request.form['pull']
        legs = request.form['legs']
        abs = request.form['abs']
        cardio = request.form['cardio']
        protien = request.form['protien']  
        date = request.form['date']      
        todo=Todo(push=push,pull=pull,legs=legs,abs=abs,cardio=cardio,protien=protien, date=date)
        db.session.add(todo)
        db.session.commit()
        return redirect("/database")
    allTodo=Todo.query.all()    
    return render_template('index.html', allTodo=allTodo)

@app.route('/database')
def products():
    allTodo=Todo.query.all()
    
    return render_template('database.html', allTodo=allTodo)

@app.route('/update/<int:sno>', methods=['GET','POST'])
def Update(sno):
    if request.method=='POST':
        push= request.form['push']
        pull = request.form['pull']
        legs = request.form['legs']
        abs = request.form['abs']
        cardio = request.form['cardio']
        protien = request.form['protien']
        date = request.form['date']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.push=push
        todo.pull=pull
        todo.legs=legs
        todo.abs=abs
        todo.cardio=cardio
        todo.protien=protien
        todo.date=date
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
    app.run(debug=True, port=3000)