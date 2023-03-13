from django.contrib.auth.models import User

from django.http import HttpRequest
from django.contrib import messages
from django.db import IntegrityError

from ..models import DataSchema, DataSchemaColumn
from ..forms import DataSchemaForm, DataSchemaColumnFormSet


def save_data_schema(form: DataSchema,
                     formset: DataSchemaColumn,
                     current_user: User,
                     request: HttpRequest) -> None:
    """
    Saves a DataSchema and its associated DataSchemaColumns
    based on the submitted form and formset and returns it.

    Args:
        form (ModelForm): The Django form representing the DataSchema.
        formset (BaseModelFormSet): The Django formset representing the DataSchemaColumns.
        current_user (User): The user making the request.
    """
    
    schema = form.save(current_user, commit=False)
    schema.save()
    formset.instance = schema
    try:
        formset.save()
    except (ValueError, IntegrityError) as e:
        messages.error(request, e)
        
    return schema
    
    
def handle_form_errors(form: DataSchemaForm,
                       formset: DataSchemaColumnFormSet,
                       request: HttpRequest) -> None:
    '''
    Add any form and formset errors to Django messages for display to the user.

    Args:
        form: The DataSchemaForm form object.
        formset: The DataSchemaColumnFormSet formset object.
        request: The current HTTP request object.
    '''
    
    for error in form.non_field_errors():
        messages.error(request, error)

    for subform in formset:
        for field, errors in subform.errors.items():
            for error in errors:
                messages.error(request, f'{subform.fields[field].label}: {error}')