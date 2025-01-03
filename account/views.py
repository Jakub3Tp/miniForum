from django.contrib import messages
from django.db.models import Avg, Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from . import models
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, ConsoleForm, CommentForm, RatingForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Console, Comment, Rating
from django.contrib.auth.mixins import LoginRequiredMixin

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(username=cleaned_data['username'],
                                password=cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Uwierzytelnienie zakończyło się suksesem')
                else:
                    return HttpResponse('Konto jest zablokowane')
            else:
                return HttpResponse('Nieprawidłowe dane logowania')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm
    return render(request,
                  'account/register.html', {'user_form': user_form})
@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Pomyślnie zaktualizowano konto')
        else:
            messages.error(request, "Nie udało się zaktualizować konta")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,'account/edit.html',
                  {'user_form': user_form, 'profile_name': profile_form})

def console_list(request):
    producenci = Console.objects.values_list('producent', flat=True).distinct()
    query = request.GET.get('q', '')
    producent_filter = request.GET.get('producent', '')
    data_premiery_from = request.GET.get('data_premiery_from', '')
    data_premiery_to = request.GET.get('data_premiery_to', '')

    consoles = Console.objects.all()

    if query:
        consoles = consoles.filter(Q(nazwa__icontains=query) | Q(opis__icontains=query))

    if producent_filter:
        consoles = consoles.filter(producent__icontains=producent_filter)

    if data_premiery_from:
        consoles = consoles.filter(data_premiery__gte=data_premiery_from)
    if data_premiery_to:
        consoles = consoles.filter(data_premiery__lte=data_premiery_to)
    return render(request, 'account/console_list.html', {'consoles': consoles, "producenci": producenci})

def add_console(request):
    if request.method == 'POST':
        form = ConsoleForm(request.POST, request.FILES)
        if form.is_valid():
            console = form.save(commit=False)
            console.autor = request.user
            form.save()
            return redirect('console_list')
    else:
        form = ConsoleForm()
    return render(request, 'account/add_console.html', {'form': form})

def edit_console(request, pk):
    console = Console.objects.get(pk=pk)
    if request.method == 'POST':
        form = ConsoleForm(request.POST, request.FILES, instance=console)
        if form.is_valid():
            form.save()
            return redirect('console_list')
    else:
        form = ConsoleForm(instance=console)
    return render(request, 'account/edit_console.html', {'form': form})

def delete_console(request, pk):
    console = Console.objects.get(pk=pk)
    if request.method == 'POST':
        console.delete()
        return redirect('console_list')
    return render(request, 'account/delete_console.html', {'console': console})

def console_detail(request, pk):
    console = Console.objects.get(pk=pk)
    comments = Comment.objects.filter(konsola=console)
    ratings = Rating.objects.filter(konsola=console)
    average_rating = ratings.aggregate(Avg('ocena'))['ocena__avg']

    user_rating = None
    if request.user.is_authenticated:
        user_rating = ratings.filter(autor=request.user).first()

    comment_form = CommentForm()
    rating_form = RatingForm()

    if request.method == 'POST' and 'comment_form' in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.konsola = console
            comment.autor = request.user
            comment.save()
            return redirect('console_detail', pk=console.pk)
    else:
        comment_form = CommentForm()

    if request.method == 'POST' and 'rating_form' in request.POST:
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            rating_data = rating_form.cleaned_data['ocena']
            if user_rating:
                user_rating.ocena = rating_data
                user_rating.save()
            else:
                new_rating = rating_form.save(commit=False)
                new_rating.konsola = console
                new_rating.autor = request.user
                new_rating.save()
            return redirect('console_detail', pk=console.pk)
    else:
        rating_form = RatingForm()

    return render(request, 'account/console_detail.html', {
        'console': console,
        'comments': comments,
        'average_rating': average_rating,
        'ratings': ratings,
        'comment_form': comment_form,
        'rating_form': rating_form,
    })
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,'account/edit.html',
                  {'user_form': user_form, 'profile_name': profile_form})
