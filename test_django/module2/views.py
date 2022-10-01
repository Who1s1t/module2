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
        name = ""
        iata = ""
        with connection.cursor() as cursor:
            cursor.execute(select_movies_query)
            result = cursor.fetchall()
            for row in result:
                if query.lower() in row[1].lower() or query.lower() in row[2].lower() or query.lower() in row[3].lower():
                    name = row[2]
                    iata = row[3]
                    break
        if name:
            return Response({"data": {"items":[{"name":name,"iata":iata}]}})
        else:
            return Response({"data":[]})