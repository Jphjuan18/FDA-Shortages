

def sql_conection():
    import pymysql
    from fda_credentials import credentials 
     # Connect to the database
    host,user,password,db = credentials()
    cnx = pymysql.connect(host=host,
                                user=user,
                                password=password,
                                db=db)
    # create cursor
    cursor=cnx.cursor()
    return cursor, cnx