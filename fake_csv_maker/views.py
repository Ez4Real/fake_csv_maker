from django.shortcuts import get_object_or_404, render, \
    redirect, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from .forms import DataSchemaColumnFormSet, DataSetForm, \
    DataSchemaForm
from .models import DataSchemaColumn, DataSet, DataSchema

from .services.business import get_current_user


@login_required
def create_schema(request):
    current_user = get_current_user(request)

    if request.method == 'POST':
        form = DataSchemaForm(request.POST)
        formset = DataSchemaColumnFormSet(request.POST, prefix="form")
        if form.is_valid() and formset.is_valid():
            schema = form.save(request.user)
            formset.instance = schema
            formset.save()
                    
            print('\n\nData schema has been created successfully.\n\n')
            return redirect('schemas_list')
        else:
            print('\n\nThere was an error creating the data schema.\n\n')
            for field, errors in form.errors.items():
                    for error in errors:
                        form.add_error(field, error)
            for form in formset:
                for field, errors in form.errors.items():
                    for error in errors:
                        form.add_error(field, error)
            return redirect('create_schema')
    
    else:
        form = DataSchemaForm()
        formset = DataSchemaColumnFormSet(prefix="form")
            
            
    return render(request, 'fake_csv/create_schema.html', {'form': form, 
                                                           'formset': formset,
                                                           'current_user': current_user})

@login_required
def schemas_list(request):
    current_user = get_current_user(request)
    
    user_schemas = DataSchema.objects.filter(created_by=current_user)
    
    return render(request, 'fake_csv/schemas_list.html', {'current_user': current_user,
                                                          'schemas': user_schemas})
    
@login_required
def schema_detail(request, schema_id):
    current_user = get_current_user(request)
    schema = get_object_or_404(DataSchema, pk=schema_id)
    related_columns = get_list_or_404(DataSchemaColumn, schema=schema)
    related_datasets = DataSet.objects.filter(schema=schema)
    
    if request.method == 'POST':
        form = DataSetForm(request.POST)
        if form.is_valid():
            dataset = form.save(schema)
            return redirect('schema_detail', schema_id=schema_id)
        else:
            for field, errors in form.errors.items():
                    for error in errors:
                        form.add_error(field, error)
    
    else:
        form = DataSetForm()

    return render(request, 'fake_csv/schema_detail.html', {'current_user': current_user,
                                                           'schema': schema,
                                                           'columns': related_columns,
                                                           'datasets': related_datasets,
                                                           'form': form})
    

@login_required
def delete_schema(request, schema_id):
    schema = get_object_or_404(DataSchema, pk=schema_id)
    schema.delete()
    
    return redirect('schemas_list')



from django.http import JsonResponse
@login_required
def generate_dataset(request):
    # Generate the data here
    data = {'status': 'success', 'message': 'Data generated successfully'}
    return JsonResponse(data)