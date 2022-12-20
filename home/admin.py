from django.contrib import admin
from .models import ChatRoomName, ChatLog

class ChatRoomNameAdmin(admin.ModelAdmin ):

    list_display = ('userIP', )

admin.site.register(ChatRoomName, ChatRoomNameAdmin)

class ChatLogAdmin(admin.ModelAdmin ):

    list_display = ('chatRoomNameObject', )

admin.site.register(ChatLog, ChatLogAdmin)


