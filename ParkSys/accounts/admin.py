from django.contrib import admin
from parking.models import ParkingSpot,ParkingInfo
# Register your models here.
admin.site.register(ParkingSpot)
admin.site.register(ParkingInfo)