from django.db import models
from django.contrib.auth.models import User

class DataSchema(models.Model):
    COMMA = ","
    SEMICOLON = ";"
    TAB = "\t"
    SPACE = " "
    PIPE = "|"

    COLUMN_SEPARATOR_CHOICES = [
        (COMMA, "Comma (,)"),
        (SEMICOLON, "Semicolon (;)"),
        (TAB, "Tab (\\t)"),
        (SPACE, "Space ( )"),
        (PIPE, "Pipe (|)"),
    ]
    
    DOUBLE_QUOTE = '"'
    SINGLE_QUOTE = "'"

    STRING_CHARACTER_CHOICES = [
        (DOUBLE_QUOTE, "Double-quote (\")"),
        (SINGLE_QUOTE, "Single-quote (')"),
    ]
    
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now=True)
    separator = models.CharField(max_length=1,
                                 choices=COLUMN_SEPARATOR_CHOICES,
                                 default=COMMA)
    qualifier = models.CharField(max_length=1,
                                 choices=STRING_CHARACTER_CHOICES,
                                 default=DOUBLE_QUOTE)

    def __str__(self):
        return self.name


class DataType(models.TextChoices):
    FULL_NAME = 'Full name'
    JOB = 'Job'
    EMAIL = 'Email'
    DOMAIN_NAME = 'Domain name'
    PHONE_NUMBER = 'Phone number'
    COMPANY_NAME = 'Company name'
    TEXT = 'Text'
    INTEGER = 'Integer'
    ADDRESS = 'Address'
    DATE = 'Date'


class DataSchemaColumn(models.Model):
    name = models.CharField(max_length=255)
    data_type = models.CharField(max_length=255, choices=DataType.choices)
    range_start = models.IntegerField(null=True, blank=True)
    range_end = models.IntegerField(null=True, blank=True)
    order = models.PositiveSmallIntegerField()
    schema = models.ForeignKey(DataSchema, on_delete=models.CASCADE)

    def __str__(self):
        return self.name