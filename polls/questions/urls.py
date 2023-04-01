from django.urls import path

from .views import question_detail_view

app_name = "questions"
urlpatterns = [
    path("<int:question_id>/", view=question_detail_view, name="question"),
]
