from flask import Flask, render_template, request

app=Flask(__name__)

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
    print("Name:",name,"Email:",email,"Password:",passw)
  return render_template("signup.html")

if(__name__ == "__main__"):
    app.run(host="0.0.0.0",debug=True)