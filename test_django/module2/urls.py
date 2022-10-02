from django.urls import path
from .views import ArticleView,reis
app_name = "articles"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('airports/', ArticleView.as_view()),
    path('flight/',reis.as_view())
]