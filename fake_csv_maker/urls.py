from django.urls import path
from fake_csv_maker import views

urlpatterns = [
    path('', views.create_schema, name='create_schema'),
    path('schemas/', views.list_schemas, name='list_schemas'),
]