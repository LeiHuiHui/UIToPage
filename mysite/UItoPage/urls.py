from django.urls import path

from . import views
app_name = "UItoPage"
urlpatterns = [
    path('', views.index, name='index'),
]