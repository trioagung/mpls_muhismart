import requests
import json

# PythonAnywhere API credentials
api_token = "3feaa0a4e0e1b6fe11a33b91e6b0bbf90b17f2c5"
username = "trioagung64"

headers = {
    "Authorization": f"Token {api_token}",
    "Content-Type": "application/json"
}

# Content untuk urls.py yang benar
urls_content = '''"""
URL configuration for mpls project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('main.urls')),
    path('panitia/', include('panitia.urls')),
]

if settings.DEBUG or True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''

# Update file
data = {"content": urls_content}
url = f"https://www.pythonanywhere.com/api/v0/user/{username}/files/path/home/{username}/mpls.muhismart/mpls/urls.py"

response = requests.post(url, headers=headers, json=data)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")

# Restart web app
restart_url = f"https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{username}.pythonanywhere.com/reload/"
restart_response = requests.post(restart_url, headers=headers)
print(f"Restart Status: {restart_response.status_code}")
print(f"Restart Response: {restart_response.text}")
