import random
import csv
import io

from typing import Any, List, Dict
from faker import Faker
from django.conf import settings
from django.db.models.query import QuerySet
from cloudinary.utils import cloudinary_url
import cloudinary.uploader as uploader


def write_csv_file(schema_columns: QuerySet, data: List[List[str]], csv_file: io.StringIO,
                   column_separator: str = ',', string_character: str = '"') -> None:
    '''
    Write CSV file with the given schema columns and data.
    
    Args:
    schema_columns (List[DataSchemaColumn]): List of DataSchemaColumn objects representing the schema columns.
    data (List[List[Any]]): List of lists representing the data to be written to the CSV file.
    file_path (str): The path where the CSV file should be written.
    column_separator (str, optional): The separator character to be used between columns. Defaults to ','.
    string_character (str, optional): The character to be used for string values. Defaults to '"'.
    '''
    
    writer = csv.writer(csv_file,
                        delimiter=column_separator,
                        quoting=csv.QUOTE_NONNUMERIC,
                        quotechar=string_character)
    header = [col.column_name for col in schema_columns]
    writer.writerow(header)
    writer.writerows(data)


def generate_fake_data(schema_columns: QuerySet,
                       num_records: int,
                       data_type: type) -> List[List[Any]]:
    '''
    Generate fake data for the given schema columns and data type.
    Args:
    schema_columns (QuerySet): List of DataSchemaColumn objects representing the schema columns.
    num_records (int): The number of fake data records to be generated.
    data_type (type): The data type to be generated.
    '''

    column_types = {
        data_type.FULL_NAME: lambda: fake.name(),
        data_type.JOB: lambda: fake.job(),
        data_type.EMAIL: lambda: fake.email(),
        data_type.DOMAIN: lambda: fake.domain_name(),
        data_type.PHONE_NUMBER: lambda: fake.phone_number(),
        data_type.COMPANY: lambda: fake.company(),
        data_type.TEXT: lambda: fake.text(),
        data_type.INTEGER: lambda: str(random.randint(col.range_start, col.range_end)) \
            if col.range_start and col.range_end else str(random.randint(0, 90)),
        data_type.ADDRESS: lambda: fake.address(),
        data_type.DATE: lambda: fake.date(),
    }
    
    fake = Faker()
    data = []
    
    for row in range(num_records):
        row_data = []
        for col in schema_columns:
            row_data.append(column_types[col.type]())
        data.append(row_data)
    
    return data


def generate_csv_data(schema_columns: QuerySet, 
                      data: List[dict], 
                      column_separator: str, 
                      string_character: str) -> io.StringIO:
    '''
    Generate CSV data based on schema columns and data.
    
    Args:
        schema_columns (QuerySet): List of schema columns.
        data (List[dict]): List of dictionaries containing data.
        column_separator (str): Separator to use between columns.
        string_character (str): Character to use for string fields.
    '''
    csv_data = io.StringIO()
    write_csv_file(schema_columns, data, csv_data,
                   column_separator=column_separator,
                   string_character=string_character)
    csv_data.seek(0)
    return csv_data


def upload_csv_file(instance,
                    csv_data: io.StringIO,
                    schema_name: str,
                    id: int) -> None:
    '''Upload a CSV file to Cloudinary.

    Args:
        csv_data (io.StringIO): The contents of the CSV file to upload.
        schema_name (str): The name of the schema that the CSV file was generated from.
        id (int): The primary key of the dataset that the CSV file belongs to.
    '''
    filename = f'{schema_name}_{id}.csv'.replace(' ', '_')
    cloudinary_file: Dict[str, Any] = uploader.upload(csv_data,
                                                      public_id=filename,
                                                      resource_type="raw",
                                                      folder=settings.STORE_CSV_FOLDER)
    instance.data_file, _ = cloudinary_url(cloudinary_file['public_id'],
                                           resource_type=cloudinary_file['resource_type'],
                                           folder=settings.STORE_CSV_FOLDER,
                                           secure=True)