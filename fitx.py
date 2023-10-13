from flask import Flask, render_template, request, flash
from database import newuser

app=Flask(__name__)
app.secret_key="ayu~7-@098jir c7^wiug"

@app.route("/")
def welcome():
  return render_template("landpg.html")

@app.route("/login",methods=['GET','POST'])
def login():
  #if request.method== 'POST':
    #email=request.form.get("Email")
    #passw=request.form.get("Passw")
  return render_template("login.html")

@app.route("/signup",methods=['GET','POST'])
def signup():
  if request.method=='POST':
    name=str(request.form.get('Name'))
    email=str(request.form.get('Email'))
    passw=str(request.form.get('Passw'))
    if len(name)<3:
      flash('Name must be greater than 2 characters')
    elif len(passw)<4:
      flash('Password must be greater than 4 characters')
    else:
      if newuser(name,email,passw):
        flash('Account created successfully!')
        
      else:
        flash('Email already registered!')
  return render_template("signup.html")

if(__name__ == "__main__"):
    app.run(host="0.0.0.0",debug=True)