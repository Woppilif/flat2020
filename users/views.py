from django.shortcuts import render, get_object_or_404, redirect
from booking.models import Booking
from payments.models import Transactions
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from users.forms import UserCreationForm, UserDocumentsForm
from django.urls import reverse_lazy
from django.views import generic
# Create your views here.

def sendToBooking(function):
    '''
        Redirect user to booked object if he has one
    '''
    def decorator(request, *args, **kwargs):
        r = Booking.extended.getCurrentUserRenta(request.user)
        if r is not None:
            if r.status == "pending":
                return redirect('booking:act',pk=r.pk)
            elif r.status == "waiting_for_capture":
                return redirect('booking:act',pk=r.pk)
        return function(request, *args, **kwargs)
    return decorator

def sendToBookingInner(function):
    '''
        Redirect user to booked object if he has one
    '''
    def decorator(request, *args, **kwargs):
        r = Booking.extended.getCurrentUserRenta(request.user)
        if r is not None:
            if r.status == "succeeded":
                return redirect('booking:opendoor',pk=r.pk)
        return function(request, *args, **kwargs)
    return decorator

def checkcard(function):
    '''
        
    '''
    def decorator(request, *args, **kwargs):
        if request.user.documents.yakey == "":
            return redirect('payments:index')
        return function(request, *args, **kwargs)
    return decorator

def checkDocuments(function):
    '''
        
    '''
    def decorator(request, *args, **kwargs):
        if request.user.documents.image_one == "" or request.user.documents.image_two == "":
            return redirect('users:documents')
        return function(request, *args, **kwargs)
    return decorator


@login_required(login_url='/accounts/login/')
def settings(request):
    rents = Booking.objects.filter(rentor=request.user).order_by('-id')[:10]
    payments = Transactions.objects.filter(user=request.user).order_by('-id')[:10]
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:settings')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/options.html', {'form': form,'rents':rents,'payments':payments})
   
@login_required(login_url='/accounts/login/')
def settings_delcard(request):
    request.user.documents.deleteCard()
    return redirect('users:settings')

def registration(request):
    if request.GET.get('ref') is not None:
        print(request.GET.get('ref'))
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(referal=request.GET.get('ref'))
            login(request, user)
            return redirect('users:documents')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registration.html', {'form': form})

@login_required(login_url='/accounts/login/')
def documents(request):
    if request.method == 'POST':
        form = UserDocumentsForm(data=request.POST, files=request.FILES,instance=request.user.documents)
        if form.is_valid():
            docs = form.save(commit=False)
            docs.save()            
            return redirect('payments:index')
    else:
        form = UserDocumentsForm()
    return render(request, 'users/documents.html', {'form': form})