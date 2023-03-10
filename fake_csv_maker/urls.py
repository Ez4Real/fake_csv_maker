from django.urls import path
from fake_csv_maker import views

urlpatterns = [
    path('', views.create_schema, name='create_schema'),
    path('schemas/', views.schemas_list, name='schemas_list'),
    path('schema-detail/<int:schema_id>/', views.schema_detail, name='schema_detail'),
    path('delete-schema/<int:schema_id>/', views.delete_schema, name='delete_schema'),
    
    path('generate-dataset/', views.generate_dataset, name='generate-dataset'),
]