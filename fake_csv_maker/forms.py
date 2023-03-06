from django import forms
from django.forms import formset_factory
from django.forms import inlineformset_factory
from .models import DataSchema, DataSchemaColumn

# Define form for creating a new DataSchema object
class DataSchemaForm(forms.ModelForm):
    # separator_choices = [(',', 'Comma'), (';', 'Semicolon'), ('\t', 'Tab'), (' ', 'Space'), ('|', 'Pipe')]
    # string_character_choices = [('"', 'Double-quote'), ("'", 'Single-quote')]

    separator = forms.ChoiceField(choices=DataSchema.COLUMN_SEPARATOR_CHOICES)
    string_character = forms.ChoiceField(choices=DataSchema.STRING_CHARACTER_CHOICES)

    class Meta:
        model = DataSchema
        fields = ['name', 'separator', 'string_character']
        
    def save(self, user, commit=True):
        instance = super().save(commit=False)
        instance.created_by = user
        if commit:
            instance.save()
        return instance

# Define form for creating a new DataSchemaColumn object
class DataSchemaColumnForm(forms.ModelForm):

    class Meta:
        model = DataSchemaColumn
        fields = ['name', 'data_type', 'range_start', 'range_end', 'order']

# Define formset for creating multiple DataSchemaColumn objects
# DataSchemaColumnFormset = formset_factory(DataSchemaColumnForm, extra=1, can_delete=True)
DataSchemaColumnFormSet = inlineformset_factory(DataSchema, DataSchemaColumn, form=DataSchemaColumnForm, extra=1, can_delete=True)
