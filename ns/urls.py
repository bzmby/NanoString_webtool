"""ns URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path

from nano.views import *

urlpatterns = [
    path('upload_files', upload_files, name='upload_files'), 
    path('qc', qc, name='qc'), 
    path('', index, name='qc'), 
    path('group_compatison', group_comparison, name='group_compatison'), 
    path('ge_volcano', ge_volcano, name='ge_volcano'), 
    path('admin/', admin.site.urls),
]
