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
    cursor.execute("select name,password from users where email='{}'".format(email))
    lst=cursor.fetchall()
    if lst[0]:
        return lst[0][1],lst[0][0]
    else:
      return "",""
  return False,False

def storeinfo(uid,age,gen,life,ht,wt,dis,aim,bmi,status):
  if con.is_connected():
    cursor=con.cursor()
    qs="insert into info values({},'{}','{}','{}',{},{},'{}','{}',{},'{}')".format(uid,age,gen,life,ht,wt,dis,aim,bmi,status)
    cursor.execute(qs)
    con.commit()
    return True
  return False