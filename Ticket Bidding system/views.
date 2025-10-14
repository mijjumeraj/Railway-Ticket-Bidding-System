from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.utils import timezone

from .models import Ticket, Bid
from .forms import BidForm

# --- Ticket Listing and Bidding View ---

@login_required
def ticket_list_and_bid(request):
    """
    Displays the list of active tickets and handles the bidding process.
    """
    # 1. Get all active tickets, ordered by creation time
    active_tickets = Ticket.objects.filter(is_active=True).order_by('travel_date')
    
    # Check if any tickets exist to display
    if not active_tickets.exists():
        messages.info(request, "Koi bhi ticket boli (bidding) ke liye uplabdh nahi hai.")
        return render(request, 'ticket_list.html', {'active_tickets': []})

    # Prepare data for rendering
    ticket_data = []
    for ticket in active_tickets:
        # Get the highest bid for the current ticket
        highest_bid = ticket.bids.all().order_by('-amount').first()
        
        # Check if the user has already placed a bid on this ticket
        user_bid = ticket.bids.filter(bidder=request.user).first()
        
        # Attach the data to the ticket object
        ticket_data.append({
            'ticket': ticket,
            'highest_bid_amount': highest_bid.amount if highest_bid else ticket.base_price,
            'user_bid_amount': user_bid.amount if user_bid else None,
            # Create a new form instance for each ticket
            'form': BidForm(ticket_instance=ticket), 
            'max_bid_display': ticket.max_bid_amount if ticket.max_bid_amount > 0 else 'N/A'
        })
    
    context = {
        'ticket_data': ticket_data,
        'user_placed_bids': Bid.objects.filter(bidder=request.user)
    }

    return render(request, 'ticket_list.html', context)


@login_required
def place_bid(request, ticket_id):
    """
    Handles the POST request when a user submits a bid.
    """
    ticket = get_object_or_404(Ticket, pk=ticket_id, is_active=True)
    
    if request.method == 'POST':
        # Pass the ticket instance to the form for validation
        form = BidForm(request.POST, ticket_instance=ticket)
        
        if form.is_valid():
            try:
                amount = form.cleaned_data['amount']
                
                # Check if the user already has a bid on this ticket
                existing_bid = Bid.objects.filter(ticket=ticket, bidder=request.user).first()
                
                if existing_bid:
                    # If bid exists, update the amount
                    existing_bid.amount = amount
                    existing_bid.bid_time = timezone.now() # Update bid time
                    existing_bid.save()
                    messages.success(request, f"Aapki boli ₹{amount} se safaltapoorvak update ho gayi hai.") # Your bid has been successfully updated.
                else:
                    # If no bid exists, create a new one
                    new_bid = form.save(commit=False)
                    new_bid.ticket = ticket
                    new_bid.bidder = request.user
                    new_bid.save()
                    messages.success(request, f"Aapki boli ₹{amount} safaltapoorvak darj ki gayi hai.") # Your bid has been successfully placed.

                # Redirect back to the main list
                return redirect('ticket_list_and_bid')
                
            except IntegrityError:
                # Catch case where a user tries to place a bid simultaneously
                messages.error(request, "Boli lagane mein koi dikkat aayi. Kripya phir se prayas karein.")
            except Exception as e:
                 messages.error(request, f"Ek anexpected error hua: {e}")
        else:
            # If validation fails, capture the error message and redirect
            # We only show the first error for simplicity
            error_message = next(iter(form.errors.values()))[0]
            messages.error(request, error_message)

    # Always redirect to the list view after POST to prevent resubmission
    return redirect('ticket_list_and_bid')


# --- Future Implementation: Ticket Detail View (Optional) ---

def ticket_detail(request, ticket_id):
    """
    Shows a detailed view of a single ticket and its bidding history.
    (This is an optional view for a more complex app)
    """
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    # Logic to display bidding history, etc.
    return render(request, 'ticket_detail.html', {'ticket': ticket})
