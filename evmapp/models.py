from django.db import models
import uuid  # Import the uuid module

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    purpose = models.CharField(max_length=200)
    contact = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Event(models.Model):
    event_name = models.CharField(max_length=200)
    organiser = models.CharField(max_length=100)
    time = models.TimeField()
    date = models.DateField()
    venue = models.CharField(max_length=200)
    theme = models.CharField(max_length=200)
    total_tickets = models.IntegerField()
    price_per_ticket = models.DecimalField(max_digits=10, decimal_places=2)
    vendors = models.ManyToManyField(Vendor)
    status = models.BooleanField(default=True) 


    def __str__(self):
        return self.event_name
    
class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    number_of_tickets = models.IntegerField()
    name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=15)
    flat_number = models.CharField(max_length=50)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    ticket_id = models.CharField(max_length=20, unique=True, default=000)
    order_id = models.CharField(max_length=50, unique=True, default=000)
    


    def __str__(self):
        return f"{self.name} - {self.event.event_name}"


class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)


class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=100, default=000)