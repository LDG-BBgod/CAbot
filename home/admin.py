from django.contrib import admin
from .models import ChatRoomName, ChatLog, Consulting

class ChatRoomNameAdmin(admin.ModelAdmin ):

    list_display = ('userIP', )

admin.site.register(ChatRoomName, ChatRoomNameAdmin)

class ChatLogAdmin(admin.ModelAdmin ):

    list_display = ('chatRoomNameObject', )

admin.site.register(ChatLog, ChatLogAdmin)

class ConsultingAdmin(admin.ModelAdmin):

    list_display = ('userIP', 'registerDate','phone')
    
admin.site.register(Consulting, ConsultingAdmin)


