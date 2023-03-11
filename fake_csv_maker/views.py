import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.contrib import messages
from django.http import JsonResponse, Http404

from .forms import DataSchemaColumnFormSet, DataSetForm, \
    DataSchemaForm
from .services.orm_requests import get_schemas_by_owner, \
    get_ordered_columns_by_schema, get_datasets_by_schema, \
    get_schema_by_id, get_dataset_by_id
from .services.utils import get_file_response

@login_required
def create_schema(request):
    current_user = get_user(request)

    if request.method == 'POST':
        form = DataSchemaForm(request.POST)
        formset = DataSchemaColumnFormSet(request.POST, prefix="form")
        if form.is_valid() and formset.is_valid():
            schema = form.save(request.user)
            formset.instance = schema
            formset.save()
                    
            messages.success(request, f'{schema} data schema has been created successfully.')
            return redirect('schema_detail', schema_id=schema.id)
        else:
            for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{form.fields[field].label}: {error}')
            for form in formset:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{form.fields[field].label}: {error}')
            return redirect('create_schema')
    else:
        form = DataSchemaForm()
        formset = DataSchemaColumnFormSet(prefix="form")
            
            
    return render(request, 'fake_csv/create_schema.html', {'current_user': current_user,
                                                           'form': form, 
                                                           'formset': formset,})
    

from django.shortcuts import get_object_or_404
from .models import DataSchema, DataSet

@login_required
def edit_schema(request, schema_id):
    current_user = get_user(request)
    schema = get_object_or_404(DataSchema, pk=schema_id)

    form = DataSchemaForm(request.POST or None)
    formset = DataSchemaColumnFormSet(request.POST or None, prefix="form")

    if form.is_valid() and formset.is_valid():
        schema = form.save(commit=False)
        schema.save()
        formset.save()
        
        messages.success(request, f'{schema} data schema has been edited successfully.')
        return redirect('schema_detail', schema_id=schema.id)
    else:
        for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{form.fields[field].label}: {error}')
        for form in formset:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{form.fields[field].label}: {error}')
    
    return render(request, 'fake_csv/create_schema.html', {'current_user': current_user,
                                                           'form': form, 
                                                           'formset': formset})
    

@login_required
def schemas_list(request):
    current_user = get_user(request)
    
    user_schemas = get_schemas_by_owner(current_user)
    
    return render(request, 'fake_csv/schemas_list.html', {'current_user': current_user,
                                                          'schemas': user_schemas})
    
@login_required
def schema_detail(request, schema_id):
    current_user = get_user(request)
    schema = get_schema_by_id(schema_id)
    related_columns = get_ordered_columns_by_schema(schema)
    related_datasets = get_datasets_by_schema(schema)
    
    if request.method == 'POST':
        form = DataSetForm(request.POST)
        if form.is_valid():
            dataset = form.save(schema)
            
            return JsonResponse({'dataset_id': dataset.id})
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{form.fields[field].label}: {(error)}')
            
    
    else:
        form = DataSetForm()

    return render(request, 'fake_csv/schema_detail.html', {'current_user': current_user,
                                                           'schema_id': schema_id,
                                                           'columns': related_columns,
                                                           'datasets': related_datasets,
                                                           'form': form})
    

@login_required
def delete_schema(request, schema_id):
    schema = get_schema_by_id(schema_id)
    schema.delete()
    
    return redirect('schemas_list')


@login_required
def generate_dataset(request):
    if request.method == 'POST':
        dataset_id = request.POST.get('dataset_id')
        if dataset_id:
            dataset = get_dataset_by_id(dataset_id)
            dataset.create_csv()
            
            return JsonResponse({'status': 'success', 'message': f'{dataset.schema} schema dataset has been generated'})
    return JsonResponse({'status': 'error', 'message': 'Error generating dataset'})



@login_required
def download_csv(request, file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = get_file_response(file_path)
            return response
    raise Http404


@login_required
def get_dataset_status(request):
    dataset_id = request.GET.get('dataset_id', None)
    if dataset_id is not None:
        dataset = get_object_or_404(DataSet, id=dataset_id)
        return JsonResponse({'status': dataset.status})
    return JsonResponse({'error': 'Missing dataset_id parameter'}, status=400)