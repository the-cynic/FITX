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
    return True
  return False

def exuser(email):
  if con.is_connected():
    cursor=con.cursor()
    cursor.execute("select email,password from users")
    lst=cursor.fetchall()
    for i in lst:
      if i[0]==email:
        return i[1]
    else:
      return ""
  return False