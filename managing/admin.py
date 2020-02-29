from django.contrib import admin
from managing.models import Devices, Partners, Workers, SystemLogs
from managing.views import openDoorAPI
# Register your models here.

def deletelog(modeladmin, request, queryset):
    #queryset.update(status='p')
    for i in queryset:
        openDoorAPI(i.channel_name,"deletelog",i.secret_key)

deletelog.short_description = "Clear log"

def open_door(modeladmin, request, queryset):
    #queryset.update(status='p')
    for i in queryset:
        openDoorAPI(i.channel_name,"open",i.secret_key)

open_door.short_description = "Open door"

def update_softare_new(modeladmin, request, queryset):
    #queryset.update(status='p')
    for i in queryset:
        openDoorAPI(i.channel_name,"updatenew",i.secret_key)
update_softare_new.short_description = "Update software [NEW]"

def update_softare(modeladmin, request, queryset):
    #queryset.update(status='p')
    for i in queryset:
        openDoorAPI(i.channel_name,"update",i.secret_key)

update_softare.short_description = "Update software [OLD]"

def get_log(modeladmin, request, queryset):
    #queryset.update(status='p')
    for i in queryset:
        openDoorAPI(i.channel_name,"sendlog",i.secret_key)
get_log.short_description = "Get log"

def get_ping(modeladmin, request, queryset):
    #queryset.update(status='p')
    for i in queryset:
        openDoorAPI(i.channel_name,"ping",i.secret_key)
get_ping.short_description = "Send ping"

class DeviceManager(admin.ModelAdmin):
    #inlines = [ChoiceInline,ChoiceInlineItems]
    list_display = ('flat','status','description','created_at')
    list_filter = ['created_at']
    search_fields = ['created_at','description','status']
    actions = [update_softare_new,update_softare,open_door,get_log,get_ping,deletelog]

admin.site.register(Partners)
admin.site.register(Workers)
admin.site.register(Devices,DeviceManager)
admin.site.register(SystemLogs)
