from booking.models import Booking
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
    return render(request,"trial/index.html",{"rents":rents})

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
def users(request):
    users = Documents.objects.filter(status=None)
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
