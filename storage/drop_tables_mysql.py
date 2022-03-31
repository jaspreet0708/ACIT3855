import mysql.connector

db_conn = mysql.connector.connect(host="acitkafka.eastus2.cloudapp.azure.com", user="user",
                                  password="Password", database="gym")

db_cursor = db_conn.cursor()

db_cursor.execute(''' 
                  DROP TABLE gym_member 
                  ''')

db_cursor.execute(''' 
                  DROP TABLE pt_session 
                  ''')

db_conn.commit()
db_conn.close()