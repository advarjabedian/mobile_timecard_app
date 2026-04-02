"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def home(request):
    return JsonResponse({
        "app": "PunchClock API",
        "status": "running",
        "endpoints": {
            "POST /api/login/": "Lookup employee by number",
            "POST /api/punch-in/": "Record a punch in",
            "POST /api/punch-out/": "Record a punch out",
            "GET /api/today/<employee_id>/": "Today's punches",
            "GET /api/status/<employee_id>/": "Current punch status",
            "GET /api/history/<employee_id>/": "Last 50 punches",
        },
    })


urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('timeclock.urls')),
]
