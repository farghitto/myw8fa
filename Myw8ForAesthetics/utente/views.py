from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login



def login_view(request):
    if request.method == 'POST':
        
        # import pdb; pdb.set_trace()
        
        username = request.POST['Username']
        password = request.POST['Password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            return redirect('home')  # Reindirizza alla pagina home dopo il login
        else:
            form_errors = {}
            if not username and not password :
                form_errors['Username'] = 'Campo Username obbligatorio'
                form_errors['Password'] = 'Campo Password obbligatorio'
            else:
                form_errors['Username'] = 'Credenziali non valide. Riprova'
                form_errors['Password'] = 'Credenziali non valide. Riprova'
                
            return render(request, 'utente/login.html', {'error': 'si','form_errors': form_errors})
    else:
        return render(request, 'utente/login.html')
    