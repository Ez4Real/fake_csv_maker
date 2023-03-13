from typing import List
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from ..models import DataSchema, DataSchemaColumn, DataSet

def get_schemas_by_owner(owner: User) -> List[DataSchema]:
    '''
    Returns a queryset of DataSchema
    objects created by the given owner.validators=[MaxValueValidator(9999)]
    '''
    return DataSchema.objects.filter(created_by=owner)

def get_schema_by_id(schema_id: int) -> DataSchema:
    '''
    Returns a DataSchema object with the given
    ID or raises a 404 error if not found.
    '''
    return get_object_or_404(DataSchema, id=schema_id)

def get_ordered_columns_by_schema(schema: DataSchema) -> List[DataSchemaColumn]:
    '''
    Returns a queryset of DataSchemaColumn objects
    for the given schema ordered by 'order' field.
    '''
    return DataSchemaColumn.objects.filter(schema=schema).order_by('order')

def get_datasets_by_schema(schema: DataSchema) -> List[DataSet]:
    '''
    Returns a queryset of DataSet objects
    related to the given schema.
    '''
    return DataSet.objects.filter(schema=schema)

def get_dataset_by_id(dataset_id: int) -> DataSet:
    '''
    Returns a DataSet object with the given
    ID or raises a 404 error if not found.
    '''
    return get_object_or_404(DataSet, id=dataset_id)