from django.urls import include, path

urlpatterns = [path("polls/", include("polls.urls"))]
