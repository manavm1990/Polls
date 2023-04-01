from django.urls import path

from .views import question_api_view

app_name = "questions"
urlpatterns = [
    path("<int:question_id>/", view=question_api_view, name="question"),
]
