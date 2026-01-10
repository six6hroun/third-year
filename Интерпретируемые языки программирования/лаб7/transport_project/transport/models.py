from django.db import models

class Drivers(models.Model):
    full_name = models.TextField()
    license_number = models.TextField(unique=True, blank=True, null=True)
    experience = models.IntegerField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    hire_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'drivers'
        managed = False

    def __str__(self):
        return self.full_name


class Routes(models.Model):
    route_number = models.TextField(unique=True)
    start_point = models.TextField()
    end_point = models.TextField()
    distance_km = models.FloatField(blank=True, null=True)
    duration_min = models.IntegerField(blank=True, null=True)
    fare_rub = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'routes'
        managed = False

    def __str__(self):
        return self.route_number


class Vehicles(models.Model):
    type = models.TextField()
    route_number = models.TextField()
    model = models.TextField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'vehicles'
        managed = False

    def __str__(self):
        return self.model or self.type


class Trips(models.Model):
    vehicle = models.ForeignKey(Vehicles, models.CASCADE, blank=True, null=True)
    driver = models.ForeignKey(Drivers, models.CASCADE, blank=True, null=True)
    route = models.ForeignKey(Routes, models.CASCADE, blank=True, null=True)
    departure_time = models.DateTimeField(blank=True, null=True)
    arrival_time = models.DateTimeField(blank=True, null=True)
    passengers_count = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'trips'
        managed = False

    def __str__(self):
        return f"{self.driver} - {self.route} - {self.departure_time}"