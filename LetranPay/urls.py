from django.urls import path
from . import views


__author__ = "Josue Isai Hernandez Sanchez"
__email__ = "josueisaihs@gmail.com"


urlpatterns = [
    path("api/enrollments/", views.Enrollments.as_view(), name="enrollmentspays"),
    path("api/enrollments/check/", views.checkEnrollmentPay, name="checkenrollmentspays"),
]