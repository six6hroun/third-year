from django.contrib import admin
from .models import Drivers, Vehicles, Routes, Trips

@admin.register(Drivers)
class DriversAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'license_number', 'experience', 'category', 'phone', 'hire_date')
    search_fields = ('full_name', 'license_number')
    list_filter = ('category', 'experience', 'hire_date')

@admin.register(Vehicles)
class VehiclesAdmin(admin.ModelAdmin):
    list_display = ('model', 'type', 'route_number', 'year', 'capacity', 'status')
    search_fields = ('model', 'route_number')
    list_filter = ('type', 'status', 'year')

@admin.register(Routes)
class RoutesAdmin(admin.ModelAdmin):
    list_display = ('route_number', 'start_point', 'end_point', 'distance_km', 'duration_min', 'fare_rub')
    search_fields = ('route_number', 'start_point', 'end_point')
    list_filter = ('distance_km',)

@admin.register(Trips)
class TripsAdmin(admin.ModelAdmin):
    list_display = ('driver', 'vehicle', 'route', 'departure_time', 'arrival_time', 'passengers_count')
    search_fields = ('driver__full_name', 'vehicle__model', 'route__route_number')
    list_filter = ('departure_time', 'arrival_time', 'route')