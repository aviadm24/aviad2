"""mysite URL Configuration

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
from home import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^google/login$', views.login, name='login'),
    url(r'^google/auth$', views.google_auth_redirect, name='google_auth_redirect'),
    url(r'^google_contacts_app$', views.google_contacts_app, name='google_contacts_app'),
    url(r'^add_contact$', views.add_contact, name='add_contact'),
    url(r'^privacy_policy$', views.privacy_policy, name='privacy_policy'),
url(r'^action_check$', views.action_check, name='action_check'),
    url(r'^pdf_booklet_demo$', views.pdf_booklet_demo, name='pdf_booklet_demo'),
    url(r'^send_mail$', views.send_mail, name='send_mail'),
    url(r'^lesson1$', views.lesson1, name='lesson1'),
    url(r'^lesson2$', views.lesson2, name='lesson2'),
    url(r'^lesson3$', views.lesson3, name='lesson3'),
    url(r'^lesson4$', views.lesson4, name='lesson4'),
    url(r'^lesson5$', views.lesson5, name='lesson5'),
]
