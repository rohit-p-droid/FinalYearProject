from django.contrib import admin
from django.urls import path
from project import views

urlpatterns = [
    path("", views.index, name="home"),
    path("about", views.about, name="about"),
    path("adminLogin", views.adminLogin, name="adminLogin"),
    path("addMonuments", views.addMonument, name="addMonuments"),
    path("viewMonuments", views.viewMonuments, name="viewMonuments"),
    path("bookTicket", views.bookTicket, name="bookTicket"),
    path("getMonument", views.getMonument, name="getMonument"),
    # path("selectCity", views.selectCity, name="selectCity"),
    # path("selectMonument", views.selectMonument, name="selectMonument"),
    path("booking", views.booking, name="booking"),
    path("ticketDetail", views.ticketDetail, name="ticketDetail"),
    path("payment", views.payment, name="payment"),
    path("success", views.success, name="success"),
    path("verify", views.verify, name="verify"),
    path("regenerateTicket", views.regenerateTicket, name="regenerateTicket"), 
    path("crowd", views.crowd, name="crowd"),
    path("viewTicket", views.viewTicket, name="viewTicket"),

]
