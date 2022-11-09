#importing Lib
import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app=Flask(__name__)

#configuration
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)
Migrate(app,db)

#model creation

class Students(db.Model):
    __tablename__='students'
    id=db.Column(db.Integer,primary_key=True)
    fname=db.Column(db.Text)
    lname=db.Column(db.Text)
    email=db.Column(db.Text)
    number=db.Column(db.Integer)
    address=db.Column(db.Text)
    gender=db.Column(db.Text)
    def __init__(self,fname,lname,email,number,address,gender):
        self.fname=fname
        self.lname=lname
        self.email=email
        self.number=number
        self.address=address
        self.gender=gender


#inserting
@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/insert',methods=['GET','POST'])
def insert():
    if request.method=='POST':
        fname=request.form.get('fname')
        lname=request.form.get('lname')
        email=request.form.get('email')
        number=request.form.get('number')
        address=request.form.get('address')
        gender=request.form.get('gender')
        data=Students(fname,lname,email,number,address,gender)
        db.session.add(data)
        db.session.commit()
        print(fname)
    return render_template('insert.html')

@app.route('/display',methods=['GET','POST'])
def display():
    details=Students.query.all()
    return render_template('display.html',details=details)


@app.route('/<int:id>/update',methods=['GET','POST'])
def update(id):
    details=Students.query.filter_by(id=id).first()
    if request.method=='POST':
        db.session.delete(details)
        db.session.commit()
        if details:

            fname=request.form.get('fname')
            lname=request.form.get('lname')
            email=request.form.get('email')
            number=request.form.get('number')
            address=request.form.get('address')
            gender=request.form.get('gender')

            details=Students(fname=fname,lname=lname,email=email,number=number,address=address,gender=gender)
            db.session.add(details)
            db.session.commit()
            return redirect('/display')
    return render_template('update.html',details=details)

@app.route('/<int:id>/delete',methods=['GET','POST'])
def delete(id):
    details=Students.query.filter_by(id=id).first()
    if request.method=='POST':
        if details:
            db.session.delete(details)
            db.session.commit()
            return redirect('/display')
        abort(404)
    return render_template('delete.html')


if __name__=='__main__':
    app.run(debug=True)
