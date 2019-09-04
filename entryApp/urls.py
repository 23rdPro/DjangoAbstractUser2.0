from django.urls import path

from . import views

urlpatterns = [

	# url(r'^', views.home_page_home, name='home'),
    path('', views.home_page_home, name='home'),


]


