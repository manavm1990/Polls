from django.urls import path

from .views import question_list_api_view, question_retrieve_api_view

app_name = "questions"
urlpatterns = [
    path("", view=question_list_api_view, name="questions"),
    path("<str:question_id>/", view=question_retrieve_api_view, name="question"),
]
