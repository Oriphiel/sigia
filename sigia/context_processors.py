from django.conf import settings # import the settings file

def report_server(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'REPORT_SERVER': settings.REPORT_SERVER}