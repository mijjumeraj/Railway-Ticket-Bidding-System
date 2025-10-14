from django.db import models
from django.contrib.auth.models import User # For linking bids to users
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

# Import the prediction logic from the service layer
from .service import predict_max_bid_amount # ML/Prediction logic

# --- Core Train Information ---
class Ticket(models.Model):
    """
    Ticket model: Represents a canceled railway ticket available for bidding.
    """
    
    # Core Train Information
    train_number = models.CharField(max_length=20, verbose_name="Train Number")
    origin = models.CharField(max_length=100, verbose_name="Origin Station")
    destination = models.CharField(max_length=100, verbose_name="Destination Station")
    travel_date = models.DateField(verbose_name="Travel Date")
    seat_class = models.CharField(max_length=50, verbose_name="Seat Class")

    # Pricing and Bidding Limits
    base_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Base Price (₹)")
    
    # This max_bid_amount is set by the ML service to cap high bids
    max_bid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="ML Max Bid (₹)", editable=False)
