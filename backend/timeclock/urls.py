from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.login_by_number, name="login"),
    path("punch-in/", views.punch_in, name="punch-in"),
    path("punch-out/", views.punch_out, name="punch-out"),
    path("history/<int:employee_id>/", views.punch_history, name="punch-history"),
    path("today/<int:employee_id>/", views.today_punches, name="today-punches"),
    path("status/<int:employee_id>/", views.current_status, name="current-status"),
]
