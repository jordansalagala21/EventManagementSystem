import uuid
import razorpay
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from evmproject import settings
from .models import Booking, Event, Vendor, Payment
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Sum, F, Min, Count
from django.db import transaction
from twilio.rest import Client
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'evmapp/register.html', {'form':form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error_message = "Invalid Credentials, Please try again"
            
    return render(request, 'evmapp/login.html', {'error_message':error_message if 'error_message' in locals() else ''})


@login_required(login_url='/login/')
def dashboard(request):
    eventcount = Event.objects.all()
    totalevents = eventcount.count()
    vendors = Vendor.objects.all()
    totalvendors = vendors.count()
    total_funds = Booking.objects.aggregate(total_funds=Sum('total_cost'))['total_funds'] or 0
    events = Event.objects.annotate(total_tickets_sold=Sum('booking__number_of_tickets'))
    
    event_labels = [event.event_name for event in events]
    tickets_sold = [event.total_tickets_sold if event.total_tickets_sold else 0 for event in events]

    events = Event.objects.annotate(total_revenue=Sum('booking__total_cost'))
    event_data = [{'event_name': event.event_name, 'total_revenue': event.total_revenue or 0} for event in events]
  
    context={
        'totalevents' :totalevents,
        'totalvendors': totalvendors,
        'total_funds': total_funds,
        'event_labels': event_labels,
        'tickets_sold': tickets_sold,
        'event_data':event_data
    }
    

    return render(request, 'evmapp/dashboard.html', context)

@login_required(login_url='/login/')
def add_event(request):
    if request.method == 'POST':
        event_name = request.POST.get('event_name')
        organiser_name = request.POST.get('organiser_name')
        time = request.POST.get('time')
        date = request.POST.get('date')
        venue = request.POST.get('venue')
        theme = request.POST.get('theme')
        total_tickets = request.POST.get('total_tickets')
        price_per_ticket = request.POST.get('price_per_ticket')

        # Create Event object
        event = Event.objects.create(
            event_name=event_name,
            organiser=organiser_name,
            time=time,
            date=date,
            venue=venue,
            theme=theme,
            total_tickets=total_tickets,
            price_per_ticket=price_per_ticket
        )

        # Handling vendors
        vendor_names = request.POST.getlist('vendor_name[]')
        purposes = request.POST.getlist('purpose[]')
        contacts = request.POST.getlist('contact[]')
        costs = request.POST.getlist('cost[]')

        for i in range(len(vendor_names)):
            vendor_name = vendor_names[i]
            purpose = purposes[i]
            contact = contacts[i]
            cost = costs[i]

            if vendor_name and purpose and contact and cost:
                vendor = Vendor.objects.create(
                    name=vendor_name,
                    purpose=purpose,
                    contact=contact,
                    cost=cost
                )
                event.vendors.add(vendor)

        messages.success(request, 'Event added successfully.')  
        return redirect('dashboard')

    return render(request, 'evmapp/add_event.html')


@login_required(login_url='/login/')
def view_event(request):
    # Assuming you have an Event model and want to fetch all events
    events = Event.objects.all()
    total_tickets_sold = Booking.objects.aggregate(total_tickets_sold=Sum('number_of_tickets'))['total_tickets_sold'] or 0
    return render(request, 'evmapp/view_events.html', {'events': events, 'total_tickets_sold':total_tickets_sold})


def send_confirmation_sms(contact_number, message):
    # Initialize Twilio client
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    # Send SMS message
    try:
        client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=contact_number
        )
    except Exception as e:
        print(f"Failed to send SMS: {str(e)}")




def ticketbooking(request):
    if request.method == 'POST':
        # Retrieve form data
        event_id = request.POST.get('event')
        event = Event.objects.get(pk=event_id)
        number_of_tickets = int(request.POST.get('number_of_tickets'))
        name = request.POST.get('name')
        contact_number = request.POST.get('contact_number')
        flat_number = request.POST.get('flat_number')
        total_cost = event.price_per_ticket * number_of_tickets

        total_cost = float(total_cost)

        # Initialize Razorpay client
        client = razorpay.Client(auth=("rzp_test_LeNsJ6Ge3PhMAU", "Kw4bOXIHHo4FYejipK8FJiBm"))

        try:
            # Create Razorpay order
            razorpay_order = client.order.create({'amount': total_cost * 100, 'currency': 'INR', 'payment_capture': '1'})
            order_id = razorpay_order['id']

            # Redirect user to Razorpay payment page
            return render(request, 'evmapp/razorpay_payment.html', {'order_id': order_id, 'total_cost': total_cost})

        except Exception as e:
            # Handle exceptions (e.g., if order creation fails)
            messages.error(request, f'Error: {str(e)}')
            return redirect('home')

    elif request.method == 'POST' and 'razorpay_payment_id' in request.POST:
        # Verify Razorpay payment
        razorpay_payment_id = request.POST['razorpay_payment_id']
        order_id = request.POST['razorpay_order_id']
        amount = request.POST['amount']

        try:
            client = razorpay.Client(auth=("rzp_test_2fQsQJ2gUiFEyX", "sjSV9iRgakbf0ZrEdZIZVSSk"))
            payment = client.payment.fetch(razorpay_payment_id)

            if payment['amount'] == int(amount) and payment['order_id'] == order_id and payment['status'] == 'captured':
                # Payment successful, create booking object
                event = Event.objects.get(pk=request.POST['event'])
                number_of_tickets = int(request.POST['number_of_tickets'])
                name = request.POST['name']
                contact_number = request.POST['contact_number']
                flat_number = request.POST['flat_number']
                total_cost = float(request.POST['total_cost'])

                with transaction.atomic():
                    ticket_id = uuid.uuid4().hex[:8].upper()
                    booking = Booking.objects.create(
                        event=event,
                        number_of_tickets=number_of_tickets,
                        name=name,
                        contact_number=contact_number,
                        flat_number=flat_number,
                        total_cost=total_cost,
                        order_id=order_id,
                        ticket_id=ticket_id
                    )

                    confirmation_message = f"Dear {name}, your booking for {number_of_tickets} ticket(s) has been confirmed. Your ticket ID is {ticket_id}. Thank you!"
                    send_confirmation_sms(contact_number, confirmation_message)
                    messages.success(request, 'Your Tickets have been booked successfully.')

                return redirect('home')
            else:
                # Payment failed or incorrect payment details
                messages.error(request, 'Payment verification failed.')
                return redirect('home')

        except Exception as e:
            # Handle exceptions
            messages.error(request, f'Error: {str(e)}')
            return redirect('home')

    else:
        # If GET request, render the form
        events = Event.objects.all()
        bookings = Booking.objects.values('name').annotate(
            id=Min('id'),
            event_id=F('event_id'),
            number_of_tickets=Sum('number_of_tickets'),
            booker_name=F('name'),
            contact_number=F('contact_number'),
            flat_number=F('flat_number'),
            total_cost=Sum('total_cost'),
            ticket_id=F('ticket_id')
        )
        return render(request, 'evmapp/ticketbooking.html', {'events': events, 'bookings': bookings})

def update_event_status(request):
    event_id = request.POST.get('event_id') 
    status = request.POST.get('status')

    try:
        event = Event.objects.get(pk=event_id)
        event.status = (status == 'active')
        event.save()
        messages.success(request, 'Event status changed successfully')
    except Event.DoesNotExist:
        messages.error(request, 'Event not found')
    return redirect('viewevent')
 
@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    total_tickets_sold = Booking.objects.aggregate(total_tickets_sold=Sum('number_of_tickets'))['total_tickets_sold'] or 0
    event_cost = event.vendors.aggregate(total_cost=Sum('cost'))['total_cost'] or 0
    money_collected = total_tickets_sold * event.price_per_ticket
    percentage_collected = (money_collected / event_cost) * 100 if event_cost else 0
    bookings = Booking.objects.filter(event=event)
    name_filter = request.GET.get('name')
    contact_number_filter = request.GET.get('contact_number')

    bookings = Booking.objects.filter(event=event)
    if name_filter:
        bookings = bookings.filter(name__icontains=name_filter)
    if contact_number_filter:
        bookings = bookings.filter(contact_number__icontains=contact_number_filter)
    return render(request, "evmapp/event_detail.html", 
                  {'event':event, 
                   'total_tickets_sold':total_tickets_sold, 
                   'event_cost':event_cost, 
                   'percentage_collected':percentage_collected,
                   'bookings':bookings})

def home(request):
    events = Event.objects.all()
    return render(request, "evmapp/home.html", {'events': events})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/login/')
def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        # Assuming you have extracted form data from request.POST manually
        event.event_name = request.POST.get('event_name')
        event.organiser = request.POST.get('organiser_name')
        event.time = request.POST.get('time')
        event.date = request.POST.get('date')
        event.venue = request.POST.get('venue')
        event.theme = request.POST.get('theme')
        # Save the event object
        event.save()
        messages.success(request, 'Event details edited successfully')
        return redirect('viewevent')
    # If it's a GET request, render the edit_event template with the event object
    return render(request, 'evmapp/edit_event.html', {'event': event})


def vendor(request):
    vendors = Vendor.objects.all()
    name_filter = request.GET.get('name')
    contact_number_filter = request.GET.get('contact_number')
    vendors = Vendor.objects.filter()
    if name_filter:
        vendors = vendors.filter(name__icontains=name_filter)
    if contact_number_filter:
        vendors = vendors.filter(contact_number__icontains=contact_number_filter)
    return render(request, 'evmapp/vendor.html', {'vendors':vendors})