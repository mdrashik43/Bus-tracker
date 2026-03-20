from django.contrib import admin
from .models import Bus, BusLocation


# Register your models here.

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'route', 'is_active']

@admin.register(BusLocation)
class BusLocationAdmin(admin.ModelAdmin):
    list_display = ['bus', 'latitude', 'longitude', 'speed', 'timestamp']
    list_filter  = ['bus']
