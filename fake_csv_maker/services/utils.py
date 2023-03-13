import os

from django.http import HttpResponse

def get_file_response(file_path: str) -> HttpResponse:
    '''
    Given a file path, returns an HttpResponse containing the
    contents of the file as an octet-stream, with the appropriate
    filename in the Content-Disposition header for downloading.
    '''
    
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response
    
