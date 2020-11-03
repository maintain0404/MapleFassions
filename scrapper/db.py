import psycopg2 as db
import secret_keys

connection = db.connect(
    database="maplefassions",
    user='maplefassions',
    password = secret_keys.db_password,
)

cur = connection.cursor()

def read(querystring):
    result = None
    try:
        cur.execute(querystring)
        result = cur.fetchall()
    except Exception as err:
        print(err)
        return
    else:
        return result

def write(querystring, values):
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

__del__ = end