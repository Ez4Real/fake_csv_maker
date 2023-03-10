from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator


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
    column_separator = models.CharField(max_length=1,
                                        choices=COLUMN_SEPARATOR_CHOICES,
                                        default=COMMA)
    string_character = models.CharField(max_length=1,
                                        choices=STRING_CHARACTER_CHOICES,
                                        default=DOUBLE_QUOTE)

    def __str__(self):
        return self.name


class DataType(models.TextChoices):
    FULL_NAME = 'Full name'
    JOB = 'Job'
    EMAIL = 'Email'
    DOMAIN = 'Domain'
    PHONE_NUMBER = 'Phone number'
    COMPANY = 'Company'
    TEXT = 'Text'
    INTEGER = 'Integer'
    ADDRESS = 'Address'
    DATE = 'Date'


class DataSchemaColumn(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=DataType.choices)
    range_start = models.IntegerField(null=True, blank=True)
    range_end = models.IntegerField(null=True, blank=True)
    order = models.PositiveSmallIntegerField()
    schema = models.ForeignKey(DataSchema, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'schema'],
                name='unique_order_per_schema'
            )
        ]


    def __str__(self):
        return self.name
    

class DataSet(models.Model):
    STATUS_READY = 'Ready'
    STATUS_PROCESSING = 'Processing'
    
    STATUS_CHOICES = [
        (STATUS_PROCESSING, "Double-quote (\")"),
        (STATUS_READY, "Single-quote (')"),
    ]
    
    schema = models.ForeignKey(DataSchema, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default=STATUS_PROCESSING)
    records = models.IntegerField(default=500,
                                  validators=[MaxValueValidator(9999)])
    data_file = models.FileField(upload_to='generated_files/',
                                 max_length=100,
                                 blank=True,
                                 null=True)