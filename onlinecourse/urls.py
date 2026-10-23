from django.urls import path
from . import views

urlpatterns = [
    path("courses/<int:course_id>/", views.course_details, name="course_details"),
    path("exams/<int:exam_id>/", views.take_exam, name="take_exam"),
    path("exams/<int:exam_id>/submit/", views.submit, name="submit"),
    path("results/<int:submission_id>/", views.show_exam_result, name="show_exam_result"),
]
