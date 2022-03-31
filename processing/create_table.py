import sqlite3 
 
conn = sqlite3.connect('stats.sqlite') 
 
c = conn.cursor() 
c.execute(''' 
          CREATE TABLE stats 
          (id INTEGER PRIMARY KEY ASC,  
           num_membership INTEGER NOT NULL, 
           num_pt_session INTEGER NOT NULL, 
           max_height FLOAT , 
           max_weight FLOAT ,  
           last_updated VARCHAR(100) NOT NULL) 
          ''') 
 
conn.commit() 
conn.close() 