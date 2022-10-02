from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
import mysql.connector
import json

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1423",
    database="module2"
)
select_movies_query = "SELECT * FROM airports LIMIT 1000"


# Create your views here.
class ArticleView(APIView):
    def get(self, request):
        query = request.GET.get("query")
        res = []
        with connection.cursor() as cursor:
            cursor.execute(select_movies_query)
            result = cursor.fetchall()
            for row in result:
                if query.lower() in row[1].lower() or query.lower() in row[2].lower() or query.lower() in row[
                    3].lower():
                    res.append({"name": row[2], "iata": row[3]})
                    break

        return Response({"data": {"items": res}})


class reis(APIView):
    def get(self, request):
        _from = request.GET.get("from")
        to = request.GET.get("to")
        date1 = request.GET.get("date1")
        date2 = request.GET.get("date2")
        flights_to = []
        flights_from = []
        with connection.cursor() as cursor:
            cursor.execute(f'select id from airports where iata like "{_from}"')
            result = cursor.fetchall()
            _from = result[0][0]
            cursor.execute(f'select id from airports where iata like "{to}"')
            result = cursor.fetchall()
            to = result[0][0]
            cursor.execute(f'select * from flights where from_id = {_from} and to_id = {to}')
            result = cursor.fetchall()
            print(result)
            for i in result:
                cursor.execute(f'select * from airports where id = "{_from}"')
                from0 = cursor.fetchall()[0]
                cursor.execute(f'select * from airports where id = "{to}"')
                to0 = cursor.fetchall()[0]
                print(from0)
                flights_to.append(
                    {"flights_id": i[0], "flights_code": i[1], "from": {"city": from0[1], "airports": from0[2],
                                                                        "iata": from0[3], "date": date1,
                                                                        "time": f"{int(i[4].total_seconds() // 3600)}:{int(i[4].total_seconds() % 3600 / 60)}"},
                     "to": {"city": to0[1], "airports": to0[2],
                            "iata": to0[3], "date": date1,
                            "time": f"{int(i[5].total_seconds() // 3600)}:{int(i[5].total_seconds() % 3600 / 60)}"},
                     "cost": i[6]})
            cursor.execute(f'select * from flights where from_id = {to} and to_id = {_from}')
            result = cursor.fetchall()
            for i in result:
                cursor.execute(f'select * from airports where id = "{to}"')
                from0 = cursor.fetchall()[0]
                cursor.execute(f'select * from airports where id = "{_from}"')
                to0 = cursor.fetchall()[0]
                flights_from.append({"flights_id": i[0], "flights_code": i[1], "from": {"city": from0[1], "airports": from0[2],
                                                                        "iata": from0[3], "date": date1,
                                                                        "time": f"{int(i[4].total_seconds() // 3600)}:{int(i[4].total_seconds() % 3600 / 60)}"},
                     "to": {"city": to0[1], "airports": to0[2],
                            "iata": to0[3], "date": date1,
                            "time": f"{int(i[5].total_seconds() // 3600)}:{int(i[5].total_seconds() % 3600 / 60)}"},
                     "cost": i[6]})

        return Response({"data": {'flights_to': flights_to,"flights_from":flights_from}})
