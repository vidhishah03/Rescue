from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import *
from .models import *
from django.contrib.auth.models import User
from .mail import send_email
from .location import lat, log, location, city, state

from django.contrib.auth.decorators import login_required


# Create your views here

def home(request):
    context = {}    
    return render(request, 'main_app/home.html', context)





def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main_app:home")


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Successfully logged in as {username} !")
                return redirect("main_app:home")
            else:
                messages.error(request, f"Invalid username or password {username} ")
        else:
            messages.error(request, "Invalid username or password  ")

    form = AuthenticationForm
    return render(request, "main_app/login.html", {'form': form})


def emergency_contact(request):
    users = User.objects.all()
    curr = 0
    for user in users:
        if request.user.is_authenticated:
            curr = user
            break
    if curr==0:
        return redirect("main_app:login")
    contacts = contact.objects.filter(user=request.user)
    total_contacts = contacts.count()
    context = {'contacts': contacts, 'total_contacts': total_contacts, 'user':request.user}
    return render(request, 'main_app/emergency_contact.html', context)


def create_contact(request):
    inst = contact(user=request.user)
    form = ContactForm(instance=inst)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=inst)
        if form.is_valid():
            form.save()
            messages.info(request, f"New contact created successfully!!")
            messages.info(request, f"An email has been sent to your contact!!")
            return redirect('main_app:emergency_contact')
        messages.error(request, f"Invalid username or password")
    context = {'form': form}
    return render(request, 'main_app/create_contact.html', context)


def update_contact(request, pk):
    curr_contact = contact.objects.get(id=pk)
    name = curr_contact.name
    form = ContactForm(initial={'name':name,'email':curr_contact.email,'relation':curr_contact.relation})
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=curr_contact)
        if form.is_valid():
            form.save()
            messages.error(request, f"{name} updated successfully!!")
            messages.info(request, f"A message has been sent to your contact!!")
            return redirect('main_app:emergency_contact')
    context = {'form': form}
    return render(request, 'main_app/create_contact.html', context)


def delete_contact(request, pk):
    curr_contact = contact.objects.get(id=pk)
    name = curr_contact.name
    if request.method == "POST":
        curr_contact.delete()
        messages.error(request, f"{name} deleted successfully!!")
        return redirect('main_app:emergency_contact')
    context = {'item': curr_contact}
    return render(request, 'main_app/delete_contact.html', context)


def emergency(request):
    users = User.objects.all()
    curr = 0
    for user in users:
        if request.user.is_authenticated:
            curr = user
            break
    if curr == 0:
        return redirect("main_app:login")
    contacts = contact.objects.filter(user=request.user)
    total_contacts = contacts.count()
    context = {'contacts': contacts, 'total_contacts': total_contacts, 'user':request.user}
    emails = []
    for j in contacts:
        emails.append(j._meta.get_field("email"))
    name = request.user.username
    link = "http://www.google.com/maps/place/"+lat+","+log
    for c in contacts:
        send_email(name, c.email, link)
    return render(request,'main_app/emergency_contact.html',context)


def helpline_numbers(request):
    return render(request, 'main_app/helpline_numbers.html', {'title': 'helpline_numbers'})


def women_laws(request):
    return render(request, 'main_app/women_laws.html', {'title': 'women_laws'})


def developers(request):
    return render(request, 'main_app/developers.html', {'title': 'developers'})


def women_rights(request):
    return render(request, 'main_app/women_rights.html', {'title': 'women_rights'})

def page_not_found(request):
    return render(request, 'main_app/404.html', {'title': '404_error'})


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Your account has been created! You are now able to log in')
#             return redirect('login')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'users/register.html', {'form': form})

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New Account Created Successfully: {username}")
            login(request, user)
            messages.info(request, f"Logged in as {username}")
            return redirect('main_app:home')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: form.error_messages[msg]")
    form = UserRegisterForm()
    return render(request, 'main_app/register.html', context={'form': form})

@login_required
def profile(request):
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('main_app:profileview')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    P = Profile.image

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'P' : P,
    } 
    return render(request, 'main_app/profile.html', context)