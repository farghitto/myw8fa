def base_template_name_context_processor(request):

    if request.user.is_authenticated:

        
        base_template_name = 'base.html'
    else:
        base_template_name = 'base_visitatori.html'

    return {
        'base_template_name': base_template_name,
    }
