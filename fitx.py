from flask import Flask, render_template, request, redirect, flash, session
from database import newuser, exuser, storeinfo, getinfo, getworkout, updateinfo, updatepass, deluser, findworkout

app = Flask(__name__)
app.secret_key = "ayu~7-@098jir c7^wiug"

@app.route("/")
def welcome():
  return render_template("landpg.html")

#authentication procedures

@app.route("/login", methods=['GET', 'POST'])
def login():
  if session:
    return redirect(r"/home")
  if request.method == 'POST':
    email = str(request.form.get("Email"))
    passw = str(request.form.get("Passw"))
    spass, name,id = exuser(email)
    print(email, passw, spass)
    if spass:
      if spass == passw:
        session["email"]=email
        session["user"]=name
        session["id"]=id
        session["pass"]=passw
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
      uid=newuser(name, email, passw)
      if uid:
        session["id"]=uid
        session["user"]=name
        session["email"]=email
        session["pass"]=passw
        return redirect(r"/info")
      else:
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
    storeinfo(session["id"],age,gen,life,ht,wt,dis,aim,bmi,status)
    return redirect("/home")
  return render_template("info.html", title="Fitx | Info", hd="Tell us more about you!", comm="SUBMIT" )

#main pages

@app.route("/home")
def home():
  if session:
    lst=getinfo(session["id"])
    return render_template("home.html", user=session["user"].split()[0], h="spotlight", info=lst)
  else:
    return redirect(r"/login")


@app.route("/workouts")
def workouts():
  if session:
    lst=getworkout()
    print(lst)
    if lst:
      return render_template("workouts.html", user=session["user"].split()[0], w="spotlight", lst=lst)
  else:
    return redirect(r"/login")

@app.route("/workoutdetails")
def workoutdetails():
  if session:
    wid=request.args["workout"]
    lst,wname=findworkout(wid)
    if lst:
      return render_template("workoutdetails.html", user=session["user"].split()[0], w="spotlight", lst=lst, wname=wname)
  else:
    return redirect(r"/login")

@app.route("/diets")
def diets():
  if session:
    return render_template("diets.html", user=session["user"].split()[0], d="spotlight")
  else:
    return redirect(r"/login")

@app.route("/dietdetails")
def dietdetails():
  if session:
    diet=request.args['diet']
    return render_template("dietdetails.html", user=session["user"].split()[0], d="spotlight", diet=diet)
  else:
    return redirect(r"/login")

@app.route("/settings")
def settings():
  if session:
    lst=getinfo(session["id"])
    return render_template("settings.html", user=session["user"].split()[0], s="spotlight", info=lst, email=session["email"])
  else:
    return redirect(r"/login")

@app.route("/changeinfo", methods=['GET', 'POST'])
def changeinfo():
  if session:
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
      updateinfo(session["id"],age,gen,life,ht,wt,dis,aim,bmi,status)
      return redirect("/settings")
    return render_template("info.html", title="Fitx | Update", hd="Enter your updated data", comm="SAVE CHANGES")
  else:
    return redirect(r"/login")

@app.route("/changepass",methods=['GET','POST'])
def changepass():
  if session:
    if request.method == 'POST':
      oldpass=str(request.form["OldPass"])
      newpass=str(request.form["NewPass"])
      if oldpass==session["pass"]:
        if updatepass(session["id"],newpass):
          session["pass"]=newpass
          return redirect("/settings")
        else:
          flash("Could not update Password. Please try again!",'error')
      else:
        flash("Wrong Password! Please enter your correct existing password",'error')
    return render_template("changepass.html")
  else:
    return redirect(r"/login")

@app.route("/delacc",methods=['GET','POST'])
def delacc():
  if session:
    if request.method == 'POST':
      email = str(request.form.get("Email"))
      passw = str(request.form.get("Passw"))
      if email == session["email"] and passw == session["pass"]:
        if deluser(session["id"]):
          return redirect("/logout")
        else:
          flash("Could not delete account! Try again.")
      else:
        flash("Wrong Email or Password! Try again",'error')
    return render_template("delacc.html")
  else:
    return redirect(r"/login")

@app.route("/logout")
def logout():
  l=list(session.keys())
  for i in l:
    session.pop(i,default=None)
  return redirect(r"/")

if (__name__ == "__main__"):
  app.run(host="0.0.0.0", debug=True)
