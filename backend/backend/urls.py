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
from django.shortcuts import render
from django.urls import include, path


def home(request):
    return render(request, "home.html")


def manifest(request):
    return JsonResponse({
        "name": "PunchClock",
        "short_name": "PunchClock",
        "description": "Employee time clock",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#0f766e",
        "icons": [
            {
                "src": "/icon-192.svg",
                "sizes": "192x192",
                "type": "image/svg+xml",
                "purpose": "any maskable",
            },
            {
                "src": "/icon-512.svg",
                "sizes": "512x512",
                "type": "image/svg+xml",
                "purpose": "any maskable",
            },
        ],
    })


def app_icon(request):
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
        <rect width="512" height="512" rx="96" fill="#0f766e"/>
        <circle cx="256" cy="240" r="130" fill="none" stroke="white" stroke-width="18"/>
        <line x1="256" y1="240" x2="256" y2="150" stroke="white" stroke-width="14" stroke-linecap="round"/>
        <line x1="256" y1="240" x2="320" y2="270" stroke="white" stroke-width="12" stroke-linecap="round"/>
        <circle cx="256" cy="240" r="10" fill="white"/>
        <text x="256" y="430" font-size="72" text-anchor="middle" fill="white" font-family="Arial,sans-serif" font-weight="bold">PUNCH</text>
    </svg>'''
    from django.http import HttpResponse
    return HttpResponse(svg, content_type="image/svg+xml")


def service_worker(request):
    js = "self.addEventListener('fetch', function(e) { e.respondWith(fetch(e.request)); });"
    from django.http import HttpResponse
    return HttpResponse(js, content_type="application/javascript")


urlpatterns = [
    path('', home, name='home'),
    path('manifest.json', manifest, name='manifest'),
    path('sw.js', service_worker, name='sw'),
    path('icon-192.svg', app_icon, name='icon-192'),
    path('icon-512.svg', app_icon, name='icon-512'),
    path('admin/', admin.site.urls),
    path('api/', include('timeclock.urls')),
]
