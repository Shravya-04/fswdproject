
from django.contrib import admin
from django.urls import include, path
from. import views

urlpatterns = [
    path("",views.account),
   path("login",views.login),
   path("signup",views.signup),
   path("donate",views.donate),
   path("pledge",views.pledge),
   path("connect",views.connect),
   path('pdf_view', views.ViewPDF.as_view(), name="pdf_view"),
]
