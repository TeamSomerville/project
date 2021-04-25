import psycopg2

def call_sp(sp, params):
    conn = None
    returnRow = None
    try:
        conn = psycopg2.connect(
            host = "172.22.152.7",
            database = "postgres",
            user = "admin",
	    password = "admin"
        )
        cur  = conn.cursor()
        converted = []
        for (x,y) in params:
           if y == "text":
             converted.append("'{}'".format(x))
           elif y == "array":
             aha = [str(z) for z in x]
             temp = ",".join(aha)
             converted.append("'{{{}}}'".format(temp))             
           else:
             raise ValueError("param datatype not specified")

        query = "CALL {0}({1});".format(sp, ",".join(converted))
        print (query)
        cur.execute(query)
        conn.commit()
        #returnRow = cur.fetchall()
        cur.close()
    except Exception as ex:
        print (ex)
    finally:
        if conn is not None:
            conn.close()

    return returnRow

def call_fn(fn, params):
    conn = None
    returnRow = None
    try:
        conn = psycopg2.connect(
            host = "172.22.152.7",
            database = "postgres",
            user = "admin",
	    password = "admin"
        )
        cur  = conn.cursor()
        converted = []
        for (x,y) in params:
           if y == "text":
             converted.append("'{}'".format(x))
           elif y == "array":
             aha = [str(z) for z in x]
             temp = ",".join(aha)
             converted.append("'{{{}}}'".format(temp))             
           else:
             raise ValueError("param datatype not specified")

        query = "select * from {0}({1});".format(fn, ",".join(converted))
        print (query)
        cur.execute(query)
        conn.commit()
        returnRow = cur.fetchall()
        cur.close()
    except Exception as ex:
        print (ex)
    finally:
        if conn is not None:
            conn.close()

    return returnRow

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
