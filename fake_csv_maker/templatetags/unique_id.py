import random

from django import template

from ..models import DataSchemaColumn

register = template.Library()

@register.simple_tag
def generate_unique_id():
    '''
    Generates a unique integer id value for a
    new instance of the specified model class.
    '''
    while True:
        unique_id = random.randint(999, 1000000)
        if not DataSchemaColumn.objects.filter(id=unique_id).exists():
            return unique_id