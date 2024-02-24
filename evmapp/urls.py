from django.contrib.auth import views as auth_views
from django.urls import path
from evmapp import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('addevent', views.add_event, name='addevent'),
    path('viewevent', views.view_event, name='viewevent'),
    path('booktickets', views.ticketbooking, name='bookticket'),
    path('update_event_status', views.update_event_status, name='update_event_status'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('edit_event/<int:event_id>/', views.edit_event, name='edit_event'),


]