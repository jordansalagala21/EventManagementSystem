from django.contrib import admin
from .models import Vendor, Event,  Booking, UserProfile, Payment

# Register your models here.
admin.site.register(Vendor)
admin.site.register(Event)
admin.site.register(Booking)
admin.site.register(UserProfile)
admin.site.register(Payment)