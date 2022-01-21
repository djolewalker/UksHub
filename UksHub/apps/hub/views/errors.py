from django.shortcuts import render

def handler404(request, exception, template_name='hub/error/404.html'):
    response = render(request, template_name, {'exception': exception})
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request, 'hub/error/500.html')
    response.status_code = 500
    return response