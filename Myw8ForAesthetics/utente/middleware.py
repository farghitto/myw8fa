from django.shortcuts import redirect, render


class ErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code >= 400:
            exception_type = None
            exception_message = None

            if hasattr(request, 'exception_raised'):

                exception_type = type(request.exception_raised).__name__
                exception_message = str(request.exception_raised)

            error_code = f"{response.status_code}"
            error_path = f"{request.path}"

            return render(request, 'utente/error_page.html', {'codice': error_code, 'path': error_path,
                                                              'tipo': exception_type, 'messaggio': exception_message})
        return response
