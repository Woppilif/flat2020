from booking.models import Booking
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from managing.forms import RentFormEx
from django.template.loader import render_to_string
from django.http import JsonResponse
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
    rents = Booking.objects.filter(trial_key__isnull=False,status=True).order_by('-created_at')
    return render(request,"trial/index.html",{"rents":rents})

@login_required(login_url='/accounts/login/')
@checkRoleManager
def save_trial_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            ff = form.save(commit=False) #
            flat =  Flats.objects.get(pk=int(request.POST.get("flat")))
            obj = Rents.renta.createRent(flat=flat,user=request.user,start=ff.start,end=ff.end)
            obj.status = True
            obj.paid = ff.paid
            obj.trial_key = str(uuid.uuid4())
            obj.save()
            access = Access.access.createPaidAccess(obj)
            print("Renta created {0}".format(obj))
            print("And access {0}".format(access))
            
            data['form_is_valid'] = True
            rents = Rents.objects.filter(trial_key__isnull=False,status=True).order_by('-start')
            data['html_book_list'] = render_to_string('trial/includes/partial_book_list.html', {
                'rents':rents, 'new':obj.pk
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