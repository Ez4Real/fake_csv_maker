import random
import csv

from typing import Any, List
from faker import Faker


def write_csv_file(schema_columns: List[dict], data: List[List[str]], file_path: str,
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
    
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file,
                            delimiter=column_separator,
                            quoting=csv.QUOTE_NONNUMERIC,
                            quotechar=string_character)
        header = [col.column_name for col in schema_columns]
        writer.writerow(header)
        writer.writerows(data)


def generate_fake_data(schema_columns,
                       num_records: int,
                       data_type: type) -> List[List[Any]]:
    '''
    Generate fake data for the given schema columns and data type.
    Args:
    schema_columns (List[DataSchemaColumn]): List of DataSchemaColumn objects representing the schema columns.
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