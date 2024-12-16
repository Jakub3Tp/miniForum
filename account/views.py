from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .forms import ConsoleForm

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Uwierzytelniono cię!')
                else:
                    return HttpResponse('Konto jest aktualnie zablokowane')
            else:
                return HttpResponse('Źle dane uwierzytelniające')
        else:
            form = LoginForm()
        return render(request, 'account/login.html', {'form': form})

@login_required
def add_console(request):
    if request.method == 'POST':
        form = ConsoleForm(request.POST)
        if form.is_valid():
            console = form.save(commit=False)
            console.add_user = request.user
            console.save()
            return redirect('mini_Forum:consoles')
        else:
            form = ConsoleForm()
        return render(request, 'mini_Forum/consoles.html', {'form': form})
