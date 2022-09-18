
# insert_shortages inserts the pandas dataframe into mysql database 
from fda_credentials import credentials 
from fda_config import sql_conection

class MySQL:
        
    def insert_shortages():
         # Connect to the database
        cursor, cnx = sql_conection()

        # Create access to pandas df
        from scraper import scrape_web
        sub_df = scrape_web()

        # Creating column list for insertion
        cols = "`,`".join([str(i) for i in sub_df.columns.tolist()])

        # Insert DataFrame recrds one by one.
        for i,row in sub_df.iterrows():
            sql = "INSERT INTO `shortages` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
            cursor.execute(sql, tuple(row))
            #print(sql) 
            #print(row)   
        
        cnx.commit()
        return print('Inserted successfully')

    def create_table():
         # Connect to the database
        cursor, cnx = sql_conection() 

        cursor.execute("CREATE TABLE shortages (Drug VARCHAR(255), Link VARCHAR(255), Status VARCHAR(255))")
        #cursor.execute("ALTER TABLE shortages ADD PRIMARY KEY (Drug)")
        cnx.commit()
        return print('Table created')
    
    def describe_table():
        # Connect to the database
        cursor, cnx = sql_conection() 

        cursor.execute('DESCRIBE shortages')
        for x in cursor:
                print(x)
        return 

    def delete_table():
       # Connect to the database
        cursor, cnx = sql_conection() 

        cursor.execute("DELETE FROM shortages WHERE Status = 'Resolved'")
        cnx.commit()

    def get_server_info():
      # Connect to the database
        cursor, cnx = sql_conection() 
        
        db_Info = cnx.get_server_info()
        return print(db_Info)

    def select_row():
        # Connect to the database
        cursor, cnx = sql_conection() 
        return
        
    def close_cnx(bool):
         # Connect to the database
        cursor, cnx = sql_conection() 
        
        if bool == True:
            cnx.close()
            return print('Connection is closed')      
        elif bool == False:
            return #print('None')

    def delete_entire_table(delete):
        # Connect to the database
        cursor, cnx = sql_conection() 

        if delete == 'DELETE':
            cursor.execute("DELETE FROM shortages WHERE Status = 'Resolved'")
            cursor.execute("DELETE FROM shortages WHERE Status = 'Currently in Shortage'")
            print('ALL TABLES DELETED')
            cnx.commit()
        else:
            return print('Incorrect command')
            
        
       

     
