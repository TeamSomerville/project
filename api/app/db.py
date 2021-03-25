import psycopg2

def connect(query):
    """ connect to the db"""
    conn  = None
    returnRow = None
    try:
        conn = psycopg2.connect(
            host = "172.22.152.7",
            database = "postgres",
            user = "admin",
	    password = "admin"
        )

        cur  = conn.cursor()
        cur.execute(query)
        returnRow = cur.fetchall()
        cur.close()
    except Exception as ex:
        print (ex)
    finally:
        if conn is not None:
            conn.close()

    return returnRow

if __name__ == '__main__':
    connect()
