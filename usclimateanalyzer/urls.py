from django.contrib import admin
from django.urls import path, include
from climateanalyzer import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test', include('climateanalyzer.urls')),
    path('', views.Index.as_view(), name='index'),
    path('sates', views.Index.as_view, name='state_index')
]