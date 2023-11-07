from os import lstat
import mysql.connector as sl
con=sl.connect(host='fitx-thecynic-ecc2.aivencloud.com',user='avnadmin',passwd='AVNS_EObxd5cqJt_eLT6DqG9',port=26647,database='defaultdb')

def newuser(name,email,passw):
  if con.is_connected():
    cursor=con.cursor()
    cursor.execute("select email from users")
    lst=cursor.fetchall()
    for i in lst:
      if i[0]==email:
        return False
    qs="insert into users(name,email,password) values('{}','{}','{}')".format(name,email,passw)
    cursor.execute(qs)
    con.commit()
    qs="select id from users where email='{}'".format(email)
    cursor.execute(qs)
    lst=cursor.fetchall()
    return lst[0][0]
  return False

def exuser(email):
  if con.is_connected():
    cursor=con.cursor()
    cursor.execute("select name,password,id from users where email='{}'".format(email))
    lst=cursor.fetchall()
    if lst[0]:
        return lst[0][1],lst[0][0],lst[0][2]
    else:
      return "","",""
  return False,False,False

def storeinfo(uid,age,gen,life,ht,wt,dis,aim,bmi,status):
  if con.is_connected():
    cursor=con.cursor()
    qs="insert into info values({},'{}','{}','{}',{},{},'{}','{}',{},'{}')".format(uid,age,gen,life,ht,wt,dis,aim,bmi,status)
    cursor.execute(qs)
    con.commit()

def updateinfo(uid,age,gen,life,ht,wt,dis,aim,bmi,status):
  if con.is_connected():
    cursor=con.cursor()
    qs="update info set age='{}',gender='{}',life='{}',height={},weight={},disease='{}',aim='{}',bmi={}, status='{}' where id={}".format(age,gen,life,ht,wt,dis,aim,bmi,status,uid)
    cursor.execute(qs)
    con.commit()
    return True
  else:
    return False
  return False

def getinfo(uid):
  if con.is_connected():
    cursor=con.cursor()
    cursor.execute("select age,gender,life,height,weight,disease,aim,bmi,status from info where id={}".format(uid))
    lst=cursor.fetchall()
    if lst:
      return lst[0]
    else:
      return False
  return False

def updatepass(uid,npass):
  if con.is_connected():
    cursor=con.cursor()
    qs="update users set password='{}' where id={}".format(npass,uid)
    cursor.execute(qs)
    con.commit()
    return True
  else:
    return False

def getworkout():
  if con.is_connected():
    cursor=con.cursor()
    cursor.execute("select Wname from workouts")
    lst=cursor.fetchall()
    wnames=[]
    if lst:
      for i in lst:
        wnames.append(i[0])
      return wnames
    else:
      return False
  return False

def findworkout(wid):
  if con.is_connected():
    cursor=con.cursor()
    cursor.execute("select exname,gif_link from wplans natural join exercises where wid={}".format(wid))
    lst=cursor.fetchall()
    cursor.execute("select wname from workouts where wid={}".format(wid))
    wname=cursor.fetchall()[0][0]
    if lst:
      return lst,wname
    else:
      return False,False
  return False,False

def deluser(uid):
  if con.is_connected():
    cursor=con.cursor()
    cursor.execute("delete from info where id={}".format(uid))
    cursor.execute("delete from users where id={}".format(uid))
    con.commit()
    return True
  return False
