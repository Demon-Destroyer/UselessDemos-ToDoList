from flask import Flask, render_template, redirect,url_for, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

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
    user_id = db.Column(db.Integer, db.ForeignKey('users.u_id'), nullable=False)

class Users(db.Model):
    __tablename__ = 'users'
    u_id = db.Column(db.Integer, primary_key=True)
    u_name = db.Column(db.String(50))
    u_email = db.Column(db.String(200), unique=True, nullable=False)
    u_password = db.Column(db.String(100), nullable=False)
    u_tasks = db.relationship("task", backref='users', lazy=True)


@app.route('/')
def login():
    return render_template("login.html")

@app.route('/user/create', methods=["POST", "GET"])
def addUser():
    if request.method == "GET":
        return render_template("createUser.html")
    else:
        name = request.form["userName"]
        email = request.form["userEmail"]
        password = request.form["password"]

        u = Users(u_name=name,u_email=email,u_password=password)
        db.session.add(u)
        db.session.commit()
        return redirect('/')

@app.route('/task/views',methods=["POST","GET"])
def viewTask():
    if request.method == "POST":
        email = request.form["userEmail"]
        password = request.form["password"]
        u = Users.query.filter_by(u_email=email).first()
        v = u.u_password
        if u and (v == password):
            return redirect('/task/view')
        else:
            return render_template("notFound.html")

# @app.route('/tasks/view/<int:user_id>')
# def tasks_for_user(user_id):
#     user = Users.query.get(user_id)
#     tasks = user.tasks
#     return render_template('tasks.html', t_d=tasks)            

@app.route('/task/view')
def viewTasks():
    data = task.query.all()
    return render_template("tasks.html", t_d = data)

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
        
        s = task(t_title=title, t_des = des, t_date = date,user_id=1)
        
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