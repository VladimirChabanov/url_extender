#!flask/bin/python
from app import app
from mysql.connector import connect, Error
import time
import sys

# Подключаемся к базе данных

app.db_connection = None

def init_db():
    try:
        print('Connection to db:', end='')
        app.db_connection = connect(host=app.config['DB_HOST_NAME'],
                             user=app.config['DB_USER'],
                             password=app.config['DB_PASSWORLD'])
        print('OK')

        print('Create db:', end='')
        create_db_query = f"CREATE DATABASE IF NOT EXISTS {app.config['DB_DATABASE']}"
        with app.db_connection.cursor() as cursor:
            cursor.execute(create_db_query)
        print('OK')

        print('Change db:', end='')                        
        use_db_query = f"USE {app.config['DB_DATABASE']}"
        with app.db_connection.cursor() as cursor:
            cursor.execute(use_db_query)
        print('OK')

        print('Create table:', end='')
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS main(
            id INT AUTO_INCREMENT PRIMARY KEY,
            url VARCHAR(255),
            alias TEXT,
            password VARCHAR(100)
            )
            """
        with app.db_connection.cursor() as cursor:
            cursor.execute(create_table_query)
            app.db_connection.commit()  
        print('OK')
        return True     
    except Error as e:
        print('Failure', e)
        app.db_connection = None
        return False

while init_db() == False and app.config['DB_CONNECT_RETRIES'] > 0:
    app.config['DB_CONNECT_RETRIES'] -= 1
    time.sleep(1)

if app.db_connection == None:
    sys.exit(1)

 
app.run(host="0.0.0.0", port=app.config['HOST_PORT'])