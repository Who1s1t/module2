import mysql.connector
connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1423",
        database="module2"
    )
select_movies_query = "SELECT * FROM airports LIMIT 5"
with connection.cursor() as cursor:
    cursor.execute(select_movies_query)
    result = cursor.fetchall()
    for row in result:
        print(row)