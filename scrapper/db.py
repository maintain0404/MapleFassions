import psycopg2 as db
import secrets

connection = db.connect(
    database="maplefassions",
    user='maplefassions',
    password = secrets.db_password,
)

cur = connection.cursor()

def read(querystring):
    result = None
    try:
        cur.execute(querystring)
        result = cur.fetch_all()
    except Exception as err:
        print(err)
        return
    else:
        return result

def create(querystring, values):
    result = None
    try:
        cur.execute(querystring, values)
        connection.commit()
    except Exception as err:
        print(err)
        raise err
    else:
        return 

def end():
    cur.close()
    connection.close()