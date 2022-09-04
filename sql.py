import mysql.connector

import mysql.connector
from hashlib import sha256
def connect():
  mydb = mysql.connector.connect(
    host="vps1.jaskula.net.pl",
    user="gutold",
    password="12345",
    database="ict"
  )

def login(user, password):
  #admin = fc8252c8dc55839967c58b9ad755a59b61b67c13227ddae4bd3f78a38bf394f7
  try:
    mydb = mysql.connector.connect(
      host="vps1.jaskula.net.pl",
      user="root",
      password="EGgFRJKPY7I3h9eU1Uyivmli0c89DwD1",
      database="ict"
    )
    mycursor = mydb.cursor()

    sql = "SELECT password FROM user WHERE login = %(login)s"
    mycursor.execute(sql, { 'login': user })

    myresult = mycursor.fetchone()[0]
    mydb.close()
    mycursor.close()
    hash = sha256(password.encode("utf-8"))
    #print(hash.hexdigest())
    if(hash.hexdigest() == myresult): return True
  except mysql.connector.Error as error:
    print("Failed {}".format(error))
  return False

def register(user, password):
  try:
    mydb = mysql.connector.connect(
      host="vps1.jaskula.net.pl",
      user="gutold",
      password="12345",
      database="ict"
    )
    mycursor = mydb.cursor()
    sql = "SELECT * FROM user WHERE login = %(login)s"
    mycursor.execute(sql, { 'login': user })
    mycursor.fetchall()
    #print(mycursor.rowcount)
    if(mycursor.rowcount != 0): return False
    
    mycursor.reset()
    sql = "INSERT INTO user VALUES (%(login)s, %(pass)s, 0)"
    hash = sha256(password.encode("utf-8")).hexdigest()
    mycursor.execute(sql, { 'login': user , 'pass': hash})

    mydb.commit()
    mydb.close()
    mycursor.close()
  except mysql.connector.Error as error:
    print("Failed {}".format(error))
  return True

#print(login( 'admin', "admin" ))
#register('tester', '1234')
