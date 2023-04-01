from django.urls import path

from .views import question_retrieve_api_view

app_name = "questions"
urlpatterns = [
    path("<str:question_id>/", view=question_retrieve_api_view, name="question"),
]
