from django.contrib import admin
from django.urls import path

from SecondAPIApp.api.employees import EmployeesView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/employees', EmployeesView.as_view()),

]
