from django.urls import path
from . import views

app_name = 'climateanalyzer'

urlpatterns = [
    path('', views.findMaxPres),
]