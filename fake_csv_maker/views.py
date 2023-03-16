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
# from .services.utils import get_file_response
from .services.form_services import handle_form_errors, \
    save_data_schema


@login_required
def create_schema(request):
    current_user = get_user(request)

    form = DataSchemaForm(request.POST or None)
    formset = DataSchemaColumnFormSet(request.POST or None)
    if request.method == 'POST':
        if form.is_valid() and formset.is_valid():
            schema = save_data_schema(form, formset,
                                      current_user, request)
                    
            messages.success(request, f'{schema} data schema has been created successfully.')
            return redirect('schema_detail', schema_id=schema.id)
        else:
            handle_form_errors(form, formset, request)
            
    return render(request, 'fake_csv/schema_form.html', {'current_user': current_user,
                                                         'form': form, 
                                                         'formset': formset,
                                                         'is_edit': False})


@login_required
def edit_schema(request, schema_id):
    current_user = get_user(request)
    schema = get_schema_by_id(schema_id)

    form = DataSchemaForm(request.POST or None, instance=schema)
    formset = DataSchemaColumnFormSet(request.POST or None, instance=schema)
    
    if request.method == 'POST':
        if form.is_valid() and formset.is_valid():
            schema = save_data_schema(form, formset,
                                      current_user, request)
            
            messages.success(request, f'{schema} data schema has been edited successfully.')
            return redirect('schema_detail', schema_id=schema.id)
        else:
            handle_form_errors(form, formset, request)
    
    return render(request, 'fake_csv/schema_form.html', {'current_user': current_user,
                                                         'form': form, 
                                                         'formset': formset,
                                                         'is_edit': True})
     

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
    
    form = DataSetForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            dataset = form.save(schema)
            
            return JsonResponse({'dataset_id': dataset.id})
        else:
            return JsonResponse({'errors': form.errors}, status=400)

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


# @login_required
# def download_csv(request, dataset_id):
#     file_path = str(get_dataset_by_id(dataset_id).data_file)
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as fh:
#             response = get_file_response(file_path)
#             return response
#     raise Http404