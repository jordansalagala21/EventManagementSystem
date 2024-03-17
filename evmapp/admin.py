from django.contrib import admin
from .models import Vendor, Event,  Booking, UserProfile, Volunteer

# Register your models here.
admin.site.site_header = 'Custom Admin Header'



admin.site.register(Vendor)
admin.site.register(Event)
admin.site.register(Booking)
admin.site.register(UserProfile)
admin.site.register(Volunteer)