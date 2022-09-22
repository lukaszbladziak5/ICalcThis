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
  try:
    mydb = mysql.connector.connect(
      host="vps1.jaskula.net.pl",
      user="gutold",
      password="12345",
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
    sql = "INSERT INTO user(login, password, license_type) VALUES (%(login)s, %(pass)s, 0)"
    hash = sha256(password.encode("utf-8")).hexdigest()
    mycursor.execute(sql, { 'login': user , 'pass': hash})

    mydb.commit()
    mydb.close()
    mycursor.close()
  except mysql.connector.Error as error:
    print("Failed {}".format(error))
  return True


def updateUserData(user, nickname, name, surname, specialization):
  try:
    mydb = mysql.connector.connect(
      host="vps1.jaskula.net.pl",
      user="gutold",
      password="12345",
      database="ict"
    )
    mycursor = mydb.cursor()


    sql = "UPDATE user SET nickname =%(nickname)s,name =%(name)s, surname= %(surname)s, specialization = %(specialization)s WHERE login = %(login)s "
    mycursor.execute(sql, {'login': user,'nickname' : nickname, 'name' : name, 'surname' : surname, 'specialization' : specialization})

    mydb.commit()
    mydb.close()
    mycursor.close()
  except mysql.connector.Error as error:
    print("Failed {}".format(error))
  return True
#print(login( 'admin', "admin" ))
#register('tester', '1234')
