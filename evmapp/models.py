from django.db import models
import uuid  # Import the uuid module

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    purpose = models.CharField(max_length=200)
    contact = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True) 

 

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
    price_per_ticket = models.DecimalField(max_digits=10, decimal_places=2, default = 0)
    vendors = models.ManyToManyField(Vendor)
    status = models.BooleanField(default=True) 
    description = models.CharField(max_length=250, default="Fun Activites Followed by Dinner, Bring Your Friends and Family along!", null=True)
    free_ticket = models.BooleanField(default=False, null = True)  # New field for indicating if the ticket is free



    def __str__(self):
        return self.event_name
    


  # Generate a random UUID and take the first 8 characters as the ticket number

 # Generate a random UUID and take the first 8 characters as the ticket number

class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    number_of_tickets = models.IntegerField()
    name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=15)
    flat_number = models.CharField(max_length=50)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=100, default='000')
    ticket_id = models.CharField(max_length=5, unique=True)  # Unique ticket ID


    


    def __str__(self):
        return f"{self.name} - {self.event.event_name}"


class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)




from django.db import models

class Volunteer(models.Model):
    name = models.CharField(max_length=100, default="John Doe")
    contact_number = models.CharField(max_length=20, default="123-456-7890")
    email = models.EmailField(default="john.doe@example.com")
    flat_number = models.CharField(max_length=20, default="A101", null = True)
    skills_interests = models.CharField(max_length=200, default="People Management")
    previous_experience = models.CharField(max_length=200, default="Organizer")
    availability_period = models.CharField(max_length=20, choices=[
        ('One-time', 'One-time'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
        ('Always', 'Always')
    ], default="One-time")
    volunteer_role = models.CharField(max_length=100, choices=[
        ('Administrative Assistant', 'Administrative Assistant'),
        ('Fundraiser', 'Fundraiser'),
        ('Marketing Coordinator', 'Marketing Coordinator'),
        ('Social Media Manager', 'Social Media Manager'),
        ('Event Planner', 'Event Planner'),
        ('Mentor', 'Mentor'),
        ('Food Distribution Coordinator', 'Food Distribution Coordinator'),
        ('Event Photographer', 'Event Photographer'),
        ('Event Videographer', 'Event Videographer'),
        ('Technical Support', 'Technical Support'),
        ('Inventory Manager', 'Inventory Manager'),
        ('Security Officer', 'Security Officer'),
        ('First Aid Provider', 'First Aid Provider'),
        ('Referee', 'Referee')
    ], default="Administrative Assistant")
    emergency_contact = models.CharField(max_length=20, default="123-456-7890")

    def __str__(self):
        return self.name
