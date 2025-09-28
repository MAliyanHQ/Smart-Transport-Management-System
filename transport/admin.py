from django.contrib import admin
from .models import BusStop, Route, Vehicle, Trip

admin.site.register(BusStop)
admin.site.register(Route)
admin.site.register(Vehicle)
admin.site.register(Trip)
