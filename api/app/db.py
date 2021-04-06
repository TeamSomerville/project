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
        print ("test")
        for (x,y) in params:
           if y == "text":
             print ("text {}".format(x))
             converted.append("'{}'".format(x))
             print ("text printed")
           elif y == "array":
             print ("array {}".format(x))
             temp = ",".join(x)
             converted.append("'{{{}}}'".format(temp))             
             print ("array printed")
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
