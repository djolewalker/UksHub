from django.shortcuts import render
import sys


def handler404(request, exception, template_name='hub/error/404.html'):
    response = render(request, template_name, {'exception': exception})
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    type_, value, traceback = sys.exc_info()
    response = render(request, 'hub/error/500.html',
                      {'type': type_, 'value': value, 'traceback': traceback})
    response.status_code = 500
    return response
