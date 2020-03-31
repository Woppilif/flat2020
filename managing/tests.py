from django.test import TestCase
from managing.views import openDoorAPI
from managing.models import Devices
import time
# Create your tests here.

count = 0

while True:
    count+=1
    i = Devices.objects.get(pk=591)
    openDoorAPI(i.channel_name,"open",i.secret_key)
    print(count)
    time.sleep(7)



    
