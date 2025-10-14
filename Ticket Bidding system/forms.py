from django import forms
from .models import Bid, Ticket
from django.core.exceptions import ValidationError

class BidForm(forms.ModelForm):
    """
    Form for users to place a bid on a ticket.
    """
    # The 'amount' field is the only field users directly interact with
    amount = forms.DecimalField(
        label="Aapki Boli Rashi (₹)", # Your Bid Amount (₹)
        min_value=0.01,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Apni boli (bid) yahan daalein', # Enter your bid here
            'class': 'form-control'
        })
    )

    class Meta:
        model = Bid
        # We only need the user to input the amount. 
        # 'ticket' and 'bidder' are set automatically in views.
        fields = ['amount']

    def __init__(self, *args, **kwargs):
        # 1. Pop the ticket_instance to get max_bid_amount for validation
        self.ticket_instance = kwargs.pop('ticket_instance', None)
        super().__init__(*args, **kwargs)

    def clean_amount(self):
        """
        Custom validation for the bid amount, checking against the Ticket's 
        base price and the ML-predicted max bid limit.
        """
        amount = self.cleaned_data.get('amount')

        if not self.ticket_instance:
            # Should not happen in production, but good for safety
            raise forms.ValidationError("Ticket jaankari upalabdh nahi hai. Kripya phir se prayas karein.") # Ticket information is not available. Please try again.

        # 1. Check against Base Price
        if amount <= self.ticket_instance.base_price:
            raise forms.ValidationError(
                f"Aapki boli Base Price (₹{self.ticket_instance.base_price}) se zyada honi chahiye." # Your bid must be greater than the Base Price
            )

        # 2. Check against ML Max Bid Limit
        # Only check max_bid_amount if it is set (greater than 0)
        if self.ticket_instance.max_bid_amount > 0 and amount > self.ticket_instance.max_bid_amount:
             raise forms.ValidationError(
                f"Aapki boli Max Bid Limit (₹{self.ticket_instance.max_bid_amount}) se zyada nahi ho sakti." # Your bid cannot exceed the Max Bid Limit
            )

        return amount
