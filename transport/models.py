from django.db import models
from users.models import User

class BusStop(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField(null=True, blank=True)  # ✅ Add Address Field

    def __str__(self):
        return self.name

class Route(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Route name
    start_stop = models.ForeignKey(BusStop, on_delete=models.CASCADE, related_name='start_routes')
    end_stop = models.ForeignKey(BusStop, on_delete=models.CASCADE, related_name='end_routes')

    def __str__(self):
        return f"{self.start_stop} to {self.end_stop}"

class Vehicle(models.Model):
    number_plate = models.CharField(max_length=15, unique=True)
    model = models.CharField(max_length=50)  # Vehicle model
    capacity = models.IntegerField()  # Number of seats
    description = models.TextField(blank=True, null=True)  # Optional details

    def __str__(self):
        return f"{self.number_plate} ({self.model})"

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now

class Assignment(models.Model):
    driver = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, limit_choices_to={'role': 'driver'})
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    travel_time = models.DurationField()
    travel_cost = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.TimeField(default=now)  # Add start_time
    end_time = models.TimeField(null=True, blank=True)  # Add end_time
    assigned_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Driver: {self.driver.username}, Vehicle: {self.vehicle.number_plate}, Route: {self.route.name}"

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Trip(models.Model):
    assignment = models.ForeignKey("Assignment", on_delete=models.CASCADE)  # Stores assignment_id

    # 🔹 **Students assigned to this trip (Max = vehicle capacity)**
    assigned_students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name="assigned_trips",
        limit_choices_to={'role': 'student'}
    )

    # 🔹 **Students currently on the bus (Subset of assigned_students)**
    onboard_students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name="onboard_trips",
        blank=True
    )

    def student_count(self):
        """Return the number of assigned students"""
        return self.assigned_students.count()

    def onboard_count(self):
        """Return the number of students currently onboard"""
        return self.onboard_students.count()

    def max_capacity(self):
        """Return the maximum capacity of the assigned vehicle"""
        return self.assignment.vehicle.capacity if self.assignment.vehicle else 0

    def __str__(self):
        return f"Trip for {self.assignment.route.name} - {self.student_count()}/{self.max_capacity()} Students"