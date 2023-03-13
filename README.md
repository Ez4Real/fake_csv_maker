# Fake CSV Maker
Data Schema Generator

## Overview
The Data Schema Generator project allows users to create any number of data schemas to create datasets with fake data. Users can build the data schema with any number of columns of any type described above. After creating the schema, the user is able to input the number of records he/she needs to generate and press the “Generate data” button.

## Technology Stack
- Python 3
- Django
- Tailwind as the UI framework
## Endpoints
The following are the endpoints that are available in the project:

- ![#1589F0]**login/** `#1589F0` : The login page where users can log in to the application.
- **logout/** : The logout page where users can log out of the application.
- **/** : The page where users can create a new data schema.
- **schemas/** : The page that lists all the created data schemas.
- **schema-detail/<int:schema_id>/** : The page that displays the details of a specific data schema.
- **edit-schema/<int:schema_id>/** : The page where users can edit an existing data schema.
- **delete-schema/<int:schema_id>/** : The page where users can delete an existing data schema.
- **dataset-download/<str:file_path>/** : The page where users can download a CSV file containing the generated data.
- **generate-dataset/** : The endpoint that generates the dataset.

## Installation
1. Clone the repository
2. Create and activate a virtual environment using your preferred tool.
3. Install the dependencies from the requirements.txt file.
4. Run the migrations using the ```python manage.py migrate``` command.
5. Create a superuser using the ```python manage.py createsuperuser``` command.
6. In a separate terminal, collect your tailwind using the ```python manage.py tailwind build```
7. Then start tailwind server by ```python manage.py tailwind start```
8. Run the server using the ```python manage.py runserver``` command.
9. Access the application in your browser at **http://localhost:8000/**

## Usage
1. Log in to the application.
2. Create a new data schema.
3. Add columns to the data schema.
4. Generate a dataset using the generated schema and the specified number of rows.
5. Download the generated CSV file.

## Contributing
Contributions to the project are not welcome. Developed exclusively for personal purposes and for general development

## Credits
This project was developed by Yevheij. Feel free to contact me at __butilka05roma@gmail.com__ for any queries or feedback.
