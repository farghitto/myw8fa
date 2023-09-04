from django.http import HttpResponse
from django.shortcuts import render


def handle_exceptions(view_func):
    def wrapped_view(request, *args, **kwargs):
        
        try:
            return view_func(request, *args, **kwargs)
        except Exception as e:
            request.exception_raised = e  # Salva l'eccezione nella richiesta
            # Puoi personalizzare la risposta di errore
            return HttpResponse(status=500)
    return wrapped_view


def handle_error_response(view_func):

    def wrapped_view(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        
        if response.status_code >= 400:

            status_code = response.status_code
            text: response.text

            context = {'codice_di_errore': status_code,
                       'dettaglio': text
                       }
            return render(request, 'utente/erroreserver.html', context)
        return response

    return wrapped_view
