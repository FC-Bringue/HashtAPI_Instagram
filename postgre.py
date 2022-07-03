import os
import psycopg2


def createConnection():
    try:
        if os.getenv("PRJ_EXECUTER") == "heroku":
            connection = psycopg2.connect(
                os.environ['DATABASE_URL'], sslmode='require')
        else:
            connection = psycopg2.connect(host=os.getenv("postgres_host"),
                                          database=os.getenv(
                                              "postgres_database"),
                                          user=os.getenv("postgres_user"),
                                          password=os.getenv("postgres_password"))
        return connection
    except:
        print("Error: Could not connect to the database")
        return None


def rowExist(connection, table, nameOfRow, row):
    cur = connection.cursor()
    cur.execute(
        "SELECT " + nameOfRow + " FROM "+table+" WHERE "+nameOfRow+" = %s", (row,))
    return cur.fetchone() is not None


def tableCheck(connection, table):
    print("Enter tableCheck")
    if connection is None:
        return None
    cursor = connection.cursor()
    # Check if results table exists, if not create it
    """ cursor.execute(
        "select exists(select * from information_schema.tables where table_name= %s)", (table,))
    doExist = cursor.fetchone()[0] """
    try:
        cursor.execute("select * from " + table)
        doExist = True
    except:
        doExist = False
    cursor.close()
    connection.commit()
    cursor = connection.cursor()
    print(doExist)
    if doExist:
        print("Table exists")
        return True
    else:
        if table == 'results':
            cursor.execute(
                "CREATE TABLE results (id serial PRIMARY KEY, hashtag varchar(255), data TEXT)")
            print("Table created")
        elif table == 'hashtagList':
            cursor.execute(
                "CREATE TABLE hashtagList (id serial PRIMARY KEY, hashtag varchar(255))")
            print("Table created")
        cursor.close()
        connection.commit()
        return True


def saveData(data, hashtag):
    print("Enter saveData")
    connection = createConnection()
    if connection is None:
        return None
    checkExistence = tableCheck(connection, 'results')
    cursor = connection.cursor()
    # save data to results table
    # Check if row actually exist
    print("hashtag: " + hashtag)
    doRowExist = rowExist(connection, "results", "hashtag", hashtag)
    print("rowExist: " + str(doRowExist))
    if doRowExist:
        cursor.execute(
            "UPDATE results SET data=%s WHERE hashtag=%s", (data, hashtag))
    else:
        cursor.execute(
            "INSERT INTO results (hashtag, data) VALUES (%s, %s)", (hashtag, data))
    cursor.close()
    connection.commit()
    connection.close()
    return True


def fetchData(hashtag):
    print("Enter fetchData")
    connection = createConnection()
    if connection is None:
        return None
    checkExistence = tableCheck(connection, 'results')
    cursor = connection.cursor()
    # fetch data from results table
    cursor.execute(
        "SELECT data FROM results WHERE hashtag = %s", (hashtag,))
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data


def getHashtagList():
    print("Enter getHashtagList")
    connection = createConnection()
    if connection is None:
        return None
    checkExistence = tableCheck(connection, 'hashtagList')
    cursor = connection.cursor()
    # fetch data from results table
    cursor.execute(
        "SELECT hashtag FROM hashtagList")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data


def findHashtag(hashtag):
    print("Enter findHashtag")
    connection = createConnection()
    if connection is None:
        return None
    checkExistence = tableCheck(connection, 'hashtagList')
    cursor = connection.cursor()
    cursor.execute(
        "SELECT hashtag FROM hashtagList WHERE hashtag = %s", (hashtag,))
    data = cursor.fetchone()
    cursor.close()
    connection.close()
    return data


def removeHashtag(hashtag):
    print("Enter removeHashtag")
    connection = createConnection()
    if connection is None:
        return None
    checkExistence = tableCheck(connection, 'hashtagList')
    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM hashtagList WHERE hashtag = %s", (hashtag,))
    cursor.close()
    connection.commit()
    connection.close()
    return True


def savehashtagList(hashtagList):
    print("Enter savehashtagList")
    connection = createConnection()
    if connection is None:
        return None
    checkExistence = tableCheck(connection, 'hashtagList')
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO hashtagList (hashtag) VALUES (%s)", (hashtagList,))
    cursor.close()
    connection.commit()
    connection.close()
    return True
