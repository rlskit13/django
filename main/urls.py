from django.conf.urls import url
from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
	#url(r'^$', views.index, name='index'),
	path("", views.homepage, name="homepage"),
	path("register/", views.register, name="register"),
	path("logout/", views.logout_request, name="logout_request"),
	path("login/", views.login_request, name="login_request"),
	path("<single_slug>", views.single_slug, name="single_slug"),
]