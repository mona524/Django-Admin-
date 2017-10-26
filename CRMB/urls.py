"""CRMB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from custom.service import custom_admin


from django.shortcuts import render

def popup_test1(request):
    return render(request,'popup_test1.html')

def popup_test2(request):
    if request.method == 'GET':
        return render(request, 'popup_test2.html')
    elif request.method == 'POST':
        name= request.POST.get('city')
        return render(request,'popup_test3.html',{'name':name})

urlpatterns = [
    url(r'^custom/', custom_admin.site.urls,),
    url('popup_test1',popup_test1),
    url('popup_test2',popup_test2),
    ]

