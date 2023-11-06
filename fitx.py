from flask import Flask, render_template, request, redirect, flash
from database import newuser, exuser, storeinfo

app = Flask(__name__)
app.secret_key = "ayu~7-@098jir c7^wiug"
userin = ""
uid=0

@app.route("/")
def welcome():
  return render_template("landpg.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    email = str(request.form.get("Email"))
    passw = str(request.form.get("Passw"))
    spass, name = exuser(email)
    print(email, passw, spass)
    if spass:
      if spass == passw:
        global userin
        userin=name
        return redirect(r"/home")
      else:
        flash("Invalid Password", 'error')
    else:
      flash("Email not registered! Try signing up instead!", 'error')
  return render_template("login.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
  if request.method == 'POST':
    name = str(request.form.get('Name'))
    email = str(request.form.get('Email'))
    passw = str(request.form.get('Passw'))
    if len(name) < 3:
      flash('Name must be greater than 2 characters!', 'error')
    elif len(email) < 4:
      flash('Email must be greater than 3 characters!', 'error')
    elif len(passw) < 8:
      flash('Password must be 8 characters or more!', 'error')
    else:
      global uid
      uid=newuser(name, email, passw)
      if uid:
        global userin
        userin=name
        return redirect("/info")
      else:
        uid=0
        flash('Email already registered! Use another email or log in!',
              'error')
  return render_template("signup.html")


@app.route("/info", methods=['GET', 'POST'])
def info():
  if request.method == 'POST':
    print(request.form)
    age=request.form["Age"]
    gen=request.form["Gender"]
    life=request.form["Life"]
    ht=float(request.form["Height"])
    wt=float(request.form["Weight"])
    dis=request.form["Disease"]
    bmi=wt/(ht*ht)
    if bmi<18.5:
      status="Underweight"
    elif bmi<25:
      status= "Normal"
    elif bmi<30:
      status="Overweight"
    else:
      status="Obese"
    aim=""
    for i in list(request.form.keys())[6:]:
      aim=aim+i+","
    aim=aim.rstrip(",")
    storeinfo(uid,age,gen,life,ht,wt,dis,aim,bmi,status)
    return redirect("/home")
  return render_template("info.html")

@app.route("/home")
def home():
  if userin:
    return render_template("home.html", user=userin.split()[0], h="spotlight")
  else:
    return redirect(r"/login")


@app.route("/workouts")
def workouts():
  if userin:
    return render_template("workouts.html", user=userin.split()[0], w="spotlight")
  else:
    return redirect(r"/login")

@app.route("/diets")
def diets():
  if userin:
    return render_template("diets.html", user=userin.split()[0], d="spotlight")
  else:
    return redirect(r"/login")

@app.route("/inspiration")
def inspiration():
  if userin:
    return render_template("inspiration.html", user=userin.split()[0], i="spotlight")
  else:
    return redirect(r"/login")

@app.route("/settings")
def settings():
  if userin:
    return render_template("settings.html", user=userin.split()[0], s="spotlight")
  else:
    return redirect(r"/login")

@app.route("/logout")
def logout():
  global userin
  userin=""
  return redirect(r"/")


if (__name__ == "__main__"):
  app.run(host="0.0.0.0", debug=True)
