import mysql.connector as sl
con=sl.connect(host='fitx-thecynic-ecc2.aivencloud.com',user='avnadmin',passwd='AVNS_EObxd5cqJt_eLT6DqG9',port=26647,database='defaultdb')

if con.is_connected():
  cursor=con.cursor()
  cursor.execute("SHOW TABLES")
  print(cursor.fetchall())
  con.commit()
  con.close()
