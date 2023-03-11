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
    schema = models.ForeignKey(DataSchema,
                               on_delete=models.CASCADE,
                               related_name='columns')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'schema'],
                name='unique_order_per_schema'
            )
        ]


    def __str__(self):
        return self.name
    
import os 
import csv
import random
from faker import Faker
from django.conf import settings


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
    records = models.IntegerField(default=500)
    data_file = models.FileField(upload_to='generated_files/',
                                 max_length=100,
                                 blank=True,
                                 null=True)
    
    def create_csv(self):
        schema_columns = DataSchemaColumn.objects.filter(schema=self.schema).order_by('order')
        # Generate fake data for each column type
        fake = Faker()
        data = []
        for row in range(self.records):
            row = []
            for col in schema_columns:
                if col.type == DataType.FULL_NAME:
                    row.append(fake.name())
                elif col.type == DataType.JOB:
                    row.append(fake.job())
                elif col.type == DataType.EMAIL:
                    row.append(fake.email())
                elif col.type == DataType.DOMAIN:
                    row.append(fake.domain_name())
                elif col.type == DataType.PHONE_NUMBER:
                    row.append(fake.phone_number())
                elif col.type == DataType.COMPANY:
                    row.append(fake.company())
                elif col.type == DataType.TEXT:
                    row.append(fake.text())
                elif col.type == DataType.INTEGER:
                    if col.range_start and col.range_end:
                        row.append(str(random.randint(col.range_start, col.range_end)))
                    else:
                        row.append(str(random.randint(0, 999)))
                elif col.type == DataType.ADDRESS:
                    row.append(fake.address())
                elif col.type == DataType.DATE:
                    row.append(fake.date())
            data.append(row)

        # Write the data to a CSV file
        filename = f'{self.schema.name}_{self.pk}.csv'
        filepath = os.path.join(settings.MEDIA_ROOT, 'generated_files', filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=self.schema.column_separator, quoting=csv.QUOTE_MINIMAL, quotechar=self.schema.string_character)
            header = [col.name for col in schema_columns]
            writer.writerow(header)
            writer.writerows(data)

        # Update the data_file field
        self.data_file = filepath
        self.status = DataSet.STATUS_READY
        self.save()