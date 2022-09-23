from django.contrib import admin
from .models import Server

# Register your models here.
@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'name', 'description', 'server_is_active')
