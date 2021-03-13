import psycopg2

def connect():
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

        cur.execute("SELECT CityName, Country from City")

        returnRow = cur.fetchone()
        while row is not None:
            print(row)
            row = cur.fetchone()

        cur.close()
    except Exception as ex:
        print (ex)
    finally:
        if conn is not None:
            conn.close()
            print ("Database connection closed")

    return returnRow

if __name__ == '__main__':
    connect()
