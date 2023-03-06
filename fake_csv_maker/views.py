from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import DataSchemaForm, DataSchemaColumnFormSet
from .models import DataSchema

def get_current_username(request):
    return request.user.username


@login_required
def create_schema(request):
    current_user = get_current_username(request)
    
    form = DataSchemaForm(request.POST or None)
    formset = DataSchemaColumnFormSet(request.POST or None, instance=DataSchema())

    if request.method == 'POST':
        if form.is_valid() and formset.is_valid():
            data_schema = form.save(commit=False)
            data_schema.created_by = request.user
            data_schema.save()
            formset.instance = data_schema
            formset.save()


            messages.success(request, 'Data schema has been created successfully.')
            return redirect('list_schemas')
        else:
            messages.error(request, 'There was an error creating the data schema.')
    else:
        # clear the formset if it is being displayed for the first time
        formset = DataSchemaColumnFormSet(instance=DataSchema())

    return render(request, 'fake_csv/create_schema.html', {'form': form, 
                                                           'formset': formset,
                                                           'current_user': current_user})

@login_required
def list_schemas(request):
    current_user = get_current_username(request)
    
    return render(request, 'fake_csv/list_schemas.html', {'current_user': current_user})
