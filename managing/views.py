from booking.models import Booking, BookingRate
from catalog.models import Flats
from payments.models import Transactions
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from managing.forms import RentFormEx
from django.template.loader import render_to_string
from django.http import JsonResponse
from users.models import Documents
from managing.models import Devices
from payments.models import Transactions
import hashlib
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from managing import consumers
import json
from managing.modules import bot
# Create your views here.

def checkRoleManager(function):
    '''
        Redirect user to booked object if he has one
    '''
    def decorator(request, *args, **kwargs):
        try:
            role = request.user.workers.role
        except:
            return redirect('catalog:map')
        if role != 1:
            return redirect('catalog:map')
        return function(request, *args, **kwargs)
    return decorator

@login_required(login_url='/accounts/login/')
@checkRoleManager
def index(request):
    rents = Booking.objects.filter(trial_key__isnull=True).order_by('-end')
    if request.method == "GET":
        if "address" in request.GET:
            rents = rents.filter(flat__address__contains=request.GET['address'])
        if "start" in request.GET and "end" in request.GET:
            if request.GET['end'] != "" and request.GET['start'] !="":
                rents = rents.filter(start__gte=request.GET['start'],end__lte=request.GET['end'])
        elif "start" in request.GET:
            if request.GET['start'] != "":
                rents = rents.filter(start__gte=request.GET['start']) 
        elif "end" in request.GET:
            if request.GET['end'] != "":
                rents = rents.filter(end__lte=request.GET['end'])
        if "rentor" in request.GET:
            rents = rents.filter(rentor__email__contains=request.GET['rentor'])
    return render(request,"trial/index.html",{"rents":rents})

@login_required(login_url='/accounts/login/')
@checkRoleManager
def flats(request):
    flats = Flats.objects.filter(partner=request.user.workers.partner)
    if request.method == "GET":
        if "address" in request.GET:
            flats = flats.filter(address__contains=request.GET['address'])
    return render(request,"trial/flats.html",{"flats":flats})

@login_required(login_url='/accounts/login/')
@checkRoleManager
def flat(request,pk):
    flat = get_object_or_404(Flats,pk=pk,partner=request.user.workers.partner)
    rents = Booking.objects.filter(flat=flat)
    booking_reviews = BookingRate.objects.filter(booking__flat__partner=request.user.workers.partner,booking__flat=flat)
    return render(request,"trial/flat.html",{"flat":flat,"rents":rents,"booking_reviews":booking_reviews})

@login_required(login_url='/accounts/login/')
@checkRoleManager
def reviews(request):
    booking_reviews = BookingRate.objects.filter(booking__flat__partner=request.user.workers.partner)
    return render(request,"trial/reviews.html",{"booking_reviews":booking_reviews})

@login_required(login_url='/accounts/login/')
@checkRoleManager
def save_trial_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save(commit=False)          
            data['form_is_valid'] = True
            rents = Booking.objects.filter(trial_key__isnull=False).order_by('-end')
            data['html_book_list'] = render_to_string('trial/includes/partial_book_list.html', {
                'rents':rents
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required(login_url='/accounts/login/')
@checkRoleManager
def trial_create(request):
    if request.method == 'POST':
        form = RentFormEx(data=request.POST)
    else:
        form = RentFormEx()
    return save_trial_form(request, form, 'trial/includes/partial_book_create.html')

@login_required(login_url='/accounts/login/')
@checkRoleManager
def trials(request):
    rents = Booking.objects.filter(trial_key__isnull=False).order_by('-end')
    return render(request,"trial/trial.html",{"rents":rents})

@login_required(login_url='/accounts/login/')
@checkRoleManager
def user_page(request,pk):
    user = get_object_or_404(User,pk=pk)
    users = Documents.objects.filter(user=user).order_by('-status')
    rents = Booking.objects.filter(rentor=user)
    transactions = Transactions.objects.filter(user=user)
    booking_reviews = BookingRate.objects.filter(booking__rentor=user)
    return render(request,"trial/users/user_page.html",{"user":user,"users":users,"rents":rents,"transactions":transactions,"booking_reviews":booking_reviews})

@login_required(login_url='/accounts/login/')
@checkRoleManager
def users(request):
    users = Documents.objects.filter().order_by('-status')
    if request.method == "GET":
        if request.GET.get("status") is not None and request.GET.get("user_id") is not None:
            user = users.filter(status=None,user_id=int(request.GET.get("user_id"))).first()
            if user is not None:
                user.status = bool(int(request.GET.get("status")))
                user.save()
            return redirect("managing:users")
    return render(request,"trial/users.html",{"users":users})

@login_required(login_url='/accounts/login/')
@checkRoleManager
def requests(request):
    pass

@login_required(login_url='/accounts/login/')
@checkRoleManager
def devices(request):
    device = Devices.objects.all()
    return render(request,"trial/devices.html",{"devices":device})

@login_required(login_url='/accounts/login/')
@checkRoleManager
def rentaInfo(request,pk):
    booking = get_object_or_404(Booking, pk = pk)
    transactions = Transactions.objects.filter(booking=booking)
    if request.method == 'POST':
        if "approve" in request.POST:
            booking.status = "succeeded"
            booking.trial_key = None
            booking.paid = True
            booking.save()
    return render(request,"trial/booking.html",{"booking":booking,"transactions":transactions})

def device(request,dkey):
    obj, created = Devices.objects.get_or_create(
        open_key = dkey
    )
    if created is True:
        data = dict()
        code = hashlib.md5()
        codex = "{0}{1}".format(dkey,obj.pk)
        code.update(codex.encode())
        obj.secret_key = code.hexdigest()
        obj.created_at = timezone.now()
        obj.save()
        data["id"] = obj.pk
        return JsonResponse(data,status=200)

def openDoorAPI(channel_name,message = "hello",appid='key'):
    print(channel_name,message,appid)
    if channel_name is None:
        return False
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.send)(channel_name, {
            'type': 'channel_message',
            'message': message,
            'appid' : appid
    })
    '''
    async_to_sync(channel_layer.group_send)("{0}".format(channel_name), {
        'type': 'channel_message',
        'message': json.dumps(message),
        'appid' : appid
    })
    '''
    return True

def sendMessageToAllAPI(flat_id,message = "hello"):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("events", {
        'type': 'channel_message',
        'message': json.dumps(message)
    })
    return True

def telegram(request,token):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        bot.telegram_webhook(json_data)
    else:
        bot.setWebhook()
    return HttpResponse(status=200)
