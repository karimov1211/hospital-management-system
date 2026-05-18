import os
import sys
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medcare_backend.settings')

startup_error = None
try:
    from django.core.wsgi import get_wsgi_application
    django_application = get_wsgi_application()
except Exception as e:
    startup_error = traceback.format_exc()

def application(environ, start_response):
    if startup_error:
        status = '500 Internal Server Error'
        response_headers = [('Content-type', 'text/plain; charset=utf-8')]
        start_response(status, response_headers)
        return [f"WSGI Startup Error:\n\n{startup_error}".encode('utf-8')]
    
    try:
        return django_application(environ, start_response)
    except Exception as e:
        err_msg = traceback.format_exc()
        status = '500 Internal Server Error'
        response_headers = [('Content-type', 'text/plain; charset=utf-8')]
        start_response(status, response_headers)
        return [f"WSGI Request Error:\n\n{err_msg}".encode('utf-8')]

