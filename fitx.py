from flask import Flask, render_template, request, flash
from database import newuser,exuser

app=Flask(__name__)
app.secret_key="ayu~7-@098jir c7^wiug"

@app.route("/")
def welcome():
  return render_template("landpg.html")

@app.route("/login",methods=['GET','POST'])
def login():
  if request.method== 'POST':
    email=str(request.form.get("Email"))
    passw=str(request.form.get("Passw"))
    spass=exuser(email)
    print(email,passw,spass)
    if spass:
      if spass==passw:
        flash("Login Successful!",'success')
        #return render_template("home.html")
      else:
        flash("Invalid Password",'error')
    else:
      flash("Email not registered! Try signing up instead!",'error')      
  return render_template("login.html")

@app.route("/signup",methods=['GET','POST'])
def signup():
  if request.method=='POST':
    name=str(request.form.get('Name'))
    email=str(request.form.get('Email'))
    passw=str(request.form.get('Passw'))
    if len(name)<3:
      flash('Name must be greater than 2 characters!','error')
    elif len(email)<4:
      flash('Email must be greater than 3 characters!','error')
    elif len(passw)<8:
      flash('Password must be 8 characters or more!','error')
    else:
      if newuser(name,email,passw):
        flash('Account created successfully!','success')
      else:
        flash('Email already registered! Use another email or log in!','error')
  return render_template("signup.html")

if(__name__ == "__main__"):
    app.run(host="0.0.0.0",debug=True)