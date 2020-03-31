from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.utils import timezone
from datetime import datetime
from managing.models import Devices, SystemLogs
from channels.db import database_sync_to_async
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = None
        self.room_name = self.scope['url_route']['kwargs']['room_name']
                
        self.device = await self.getDevice(self.room_name)
        if self.device is not None:
            self.room_group_name = 'partner_%s' % self.device[2]
            #await self.channel_layer.group_add('events', self.channel_name) use it for global messages
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            print(self.channel_name)
            await self.setDeviceStatus(self.device[0],True,self.channel_name)
            await self.accept()
            
            print("=== Connected Device ID: {0} by Partner ID: {1} at {2}".format(self.room_name,self.room_group_name,datetime.now()))
        else:
            await self.disconnect(close_code=100)

    async def disconnect(self, close_code):
        # Leave room group
        if self.room_group_name is not None:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            await self.setDeviceStatus(self.device[0],False,self.channel_name)
            await self.addLog(self.room_name,comment="Disconnected")
            print("Disconnect {0} {1}".format(self.room_group_name,datetime.now()))
        else:
            await self.addLog(self.room_name,comment="Connection rejected")
        

    @database_sync_to_async
    def getDevice(self,id):
        try:
            device = Devices.objects.get(pk=id)
            return device, device.flat, device.flat.partner.pk
        except:
            return None

    @database_sync_to_async
    def setDeviceStatus(self,device,status,channel_name):
        device.update(status,channel_name)
        return True

    @database_sync_to_async
    def addLog(self,id,comment):
        SystemLogs.objects.create(device_id=int(id),created_at=timezone.now(),comment=comment)
        return True

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = text_data
        message = text_data#text_data_json['message']
        print("Received new message form {0}, {1}".format(self.room_group_name,message))
        await self.addLog(self.room_name,comment=message)
        # Send message to room group
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': "{0} {1} {2}".format(message,datetime.now(),self.room_name)
            }
        )
        

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
    
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
    

    async def channel_message(self, event):
        print(event)
        message = event['message']
        appid = event['appid']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'appid':appid,
            #'TEMP_KEY': self.auth_key
        }))

class BotConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = None
        self.room_name = self.scope['url_route']['kwargs']['room_name']
                
        self.device = await self.getDevice(self.room_name)
        if self.device is not None:
            self.room_group_name = 'partner_%s' % self.device[2]
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            print(self.channel_name)
            await self.accept()
            print("=== Connected BOT ID: {0} by Partner ID: {1} at {2}".format(self.room_name,self.room_group_name,datetime.now()))

    async def disconnect(self, close_code):
        # Leave room group
        if self.room_group_name is not None:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    @database_sync_to_async
    def getDevice(self,id):
        try:
            device = Devices.objects.get(pk=id)
            return device, device.flat, device.flat.partner.pk
        except:
            return None
            
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = text_data
        message = text_data#text_data_json['message']
        print("Received new message form {0}, {1}".format(self.room_group_name,message))
        # Send message to room group
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': "{0} {1} {2}".format(message,datetime.now(),self.room_name)
            }
        )
        

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
    
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))