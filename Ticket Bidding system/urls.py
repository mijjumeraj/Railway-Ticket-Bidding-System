from django.urls import path
from . import views

urlpatterns = [
    # Main listing page: Shows all active tickets and bidding forms
    path('', views.ticket_list_and_bid, name='ticket_list_and_bid'),
    
    # URL for placing a bid on a specific ticket
    # The <int:ticket_id> captures the primary key of the ticket
    path('bid/<int:ticket_id>/', views.place_bid, name='place_bid'),
    
    # Optional: Detail view for a single ticket (if implemented later)
    # path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
]
