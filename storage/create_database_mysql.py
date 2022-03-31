import mysql.connector

db_conn = mysql.connector.connect(host="acitkafka.eastus2.cloudapp.azure.com", user="user",
                                  password="Password", database="gym")

db_cursor = db_conn.cursor()

db_cursor.execute('''
          CREATE TABLE gym_member
          (id INT NOT NULL AUTO_INCREMENT, 
           user_id VARCHAR(250) NOT NULL,
           gym_address VARCHAR(250) NOT NULL,
           start_date VARCHAR(100) NOT NULL,
           membership_months INTEGER NOT NULL,
            user_name VARCHAR(250) NOT NULL,
           user_height FLOAT NOT NULL,
           user_weight FLOAT NOT NULL,
           user_address VARCHAR(250) NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           trace_id VARCHAR(250) NOT NULL,
           CONSTRAINT gym_member_pk PRIMARY KEY (id))
          ''')


db_cursor.execute('''
          CREATE TABLE pt_session
          (id INT NOT NULL AUTO_INCREMENT, 
           user_id VARCHAR(250) NOT NULL,
           trainer_id VARCHAR(250) NOT NULL,
           start_time VARCHAR(100) NOT NULL,
           duration_hours FLOAT NOT NULL,
            user_name VARCHAR(250) NOT NULL,
           user_height FLOAT NOT NULL,
           user_weight FLOAT NOT NULL,
           user_address VARCHAR(250) NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           trace_id VARCHAR(250) NOT NULL,
           CONSTRAINT pt_session_pk PRIMARY KEY (id))
          ''')

db_conn.commit()
db_conn.close()
