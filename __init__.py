from flask import Flask,redirect,url_for,render_template
from flask import *
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import main as m

app = Flask(__name__)
app.secret_key="lmas"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


users1=[]

class chat(db.Model):
    _id = db.Column("id",db.Integer,primary_key=True)
    name = db.Column("name",db.String(100))
    email = db.Column("email",db.String(100))
    password = db.Column("password",db.String(100))

    def __init__(self,name,email,password):
        self.name = name
        self.email = email
        self.password = password

class newusr(db.Model):
    _id = db.Column("id",db.Integer,primary_key=True)
    name = db.Column("name",db.String(100))
    accept = db.Column("accept",db.String(100))

    def __init__(self,name,accept):
        self.name = name
        self.accept = accept



@app.route('/')
def login():
    if "email" in session:
        return redirect(url_for('mainpage'))
    return render_template('login.html')

@app.route('/register')
def regis():
    
    return render_template('regist.html')

@app.route('/Main')
def main():
    return render_template('main.html')

@app.route("/save",methods = ["POST","GET"])  
def saveDetails():  
    msg = "msg"  
    if request.method == "POST":  
        session.permanent = True  
        name = request.form["name"]  
        password = request.form["password"] 
        email = request.form["email"]  
        print(name,password,email)
        session["email"] = email
        session["name"] = name
        if name=="" and password=="" and email=="":
            return f"Enter the fields or fields should not be empty"
        else:
            for i in chat.query.all():
                if i.name==name:
                    return f"Name or emailid is already taken"
                else:
                    usr = chat(name,email,password)
                    print(usr,name,password,email)
                    db.session.add(usr)
                    db.session.commit()
                    msg = "Login successfully Added" 
                    flash(msg)
                    return redirect(url_for("mainpage")) 
          
    else:
        return render_template('login.html') 
    return render_template('login.html')

@app.route("/verify",methods = ["POST","GET"])  
def verify():  
    msg = "msg"  
    veri = False
    very = False
    users1=[]
    if request.method == "POST":  
        name = request.form["name"]  
        password = request.form["password"] 
        print(len(chat.query.all()))
        for i in chat.query.all():
            session["email"] = i.email
            session["name"] = i.name
            if name == i.name and password == i.password:
                veri = True 
                very = False
                break
            else:
                very = True
        
        for i in chat.query.all():
            if name!=i.name:
                users1.append(i.name)
        session["userres"] = users1
        if very:
             return f'Create a Account to login or Wrong username or password'
        elif veri:
            return redirect(url_for('mainpage'))
    else:
        return render_template('login.html')
    return render_template('login.html')



@app.route("/Mainpage")
def mainpage():
    if "email" in session:
        return render_template("main.html",name=session["name"],email=session["email"],user=session["userres"])
    else:
        return render_template('login.html')
@app.route("/logout")
def logout():
    session.pop("name",None)
    session.pop("password",None)
    return render_template('login.html')

@app.route('/accept/<string:name>', methods=['GET','POST'])
def accept(name):
    print(session.pop(name))
    return redirect(url_for("mainpage"))
    

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)