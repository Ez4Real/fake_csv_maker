from django import forms
from django.forms import inlineformset_factory
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import DataSchemaColumn, \
    DataType, DataSchema, DataSet
    

SELECT_WG = forms.Select(attrs={'class': 'w-%44 base-field'})
NUMBER_INPUT = forms.NumberInput(attrs={'class': 'w-84 base-field'})


class DataSchemaForm(forms.ModelForm):
    name = forms.CharField(label='Name',
                           widget=forms.TextInput(attrs={'class': 'w-%44 base-field'}))
    column_separator = forms.ChoiceField(choices=DataSchema.COLUMN_SEPARATOR_CHOICES,
                                         widget=SELECT_WG)
    string_character = forms.ChoiceField(choices=DataSchema.STRING_CHARACTER_CHOICES,
                                         widget=SELECT_WG)

    class Meta:
        model = DataSchema
        fields = ['name', 'column_separator', 'string_character']
        
    def save(self, user, commit=True):
        instance = super().save(commit=False)
        instance.created_by = user
        if commit:
            instance.save()
        return instance


class DataSchemaColumnForm(forms.ModelForm):
    type_choices = [
        ('', '-----'), 
        (DataType.FULL_NAME, 'Full name'),
        (DataType.JOB, 'Job'),
        (DataType.EMAIL, 'Email'),
        (DataType.DOMAIN, 'Domain'),
        (DataType.PHONE_NUMBER, 'Phone number'),
        (DataType.COMPANY, 'Company'),
        (DataType.TEXT, 'Text'),
        (DataType.INTEGER, 'Integer'),
        (DataType.ADDRESS, 'Address'),
        (DataType.DATE, 'Date'),
    ]
        
    name = forms.CharField(label='Column name',
                           widget=forms.TextInput(attrs={'class': 'base-field w-80'}))
    type = forms.ChoiceField(label='Type',
                             choices=type_choices,
                             widget=forms.Select(
                                 attrs={'class': 'base-field type-field w-80'}
                             ),
                             initial='')
    range_start = forms.IntegerField(label='From',
                                     widget=NUMBER_INPUT,
                                     required=False)
    range_end = forms.IntegerField(label='To',
                                   widget=NUMBER_INPUT,
                                   required=False)
    order = forms.IntegerField(label='Order',
                               widget=forms.NumberInput(attrs={'class': 'w-40 base-field'}),
                               validators = [MinValueValidator(0)])
    
    class Meta:
        model = DataSchemaColumn
        fields = ['name', 'type', 'range_start', 'range_end', 'order']
        

DataSchemaColumnFormSet = inlineformset_factory(
                            DataSchema,
                            DataSchemaColumn,
                            form=DataSchemaColumnForm,
                            extra=1,
                            can_delete=True,
                          )


class DataSetForm(forms.ModelForm):
    class Meta:
        model = DataSet
        fields = ['records']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        records = self.fields['records']
        records.label = 'Rows'
        records.widget.attrs.update(
            {'class': 'base-field w-24 mr-2 ml-3'}
        )
        records.validators = [MinValueValidator(1),
                              MaxValueValidator(9999)]
    
    def save(self, schema, commit=True):
        instance = super().save(commit=False)
        instance.schema = schema
        if commit:
            instance.save()
        return instance