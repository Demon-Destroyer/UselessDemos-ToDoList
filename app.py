from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ToDoTaskListDB.sqlite'
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

class task(db.Model):
    __tablename__ = 'tasks'
    t_id = db.Column(db.Integer, primary_key=True)
    t_title = db.Column(db.String(100), unique=True, nullable=False)
    t_des = db.Column(db.String(500))
    t_date = db.Column(db.String(50))

@app.route('/')
def login():
    return render_template("login.html")

@app.route('/task/view')
def viewTask():
    data = task.query.all()
    return render_template("tasks.html", t_d = data)

@app.route('/task/create')
def createTask():
    return render_template("createTask.html")

@app.route('/task/create', methods=["POST","GET"])
def addTask():
    if request.method == "GET":
        return render_template("createTask.html")
    else:
        title = request.form["taskTitle"]
        
        if task.query.filter(task.t_title == title).first():
            return render_template("taskExits.html", data="s")
        
        des = request.form["taskDes"]
        date = request.form["taskDate"]
        
        s = task(t_title=title, t_des = des, t_date = date)
        
        db.session.add(s)
        db.session.commit()
        
        return redirect('/task/create')

@app.route('/task/<int:tid>/update', methods=["POST","GET"])
def updateTask(tid):
    if request.method == "GET":
        data = task.query.filter(task.t_id == tid).first()
        return render_template("updateTask.html", t_d=data)
    else:
        new = task.query.filter_by(t_id=tid).first()
        
        new.t_des = request.form["taskDes"]
        new.t_date = request.form["taskDate"]
        
        db.session.commit()
        return redirect('/task/view')
    
@app.route('/task/<int:tid>/delete')
def deleteTask(tid):
    data = task.query.filter(task.t_id == tid).first()
    db.session.delete(data)
    db.session.commit()
    return redirect('/task/view')    

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)