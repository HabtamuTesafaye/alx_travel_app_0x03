# listings/tasks.py
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

@shared_task
def send_booking_email(to_email, booking_id):
    from .models import Booking
    booking = Booking.objects.get(booking_id=booking_id)
    
    subject = f'Booking Confirmation #{booking.booking_id}'
    
    # Render HTML template
    html_content = render_to_string(
        'emails/booking_confirmation.html',
        {
            'guest_name': booking.guest.get_full_name() or booking.guest.username,
            'booking_id': booking.booking_id,
            'check_in': booking.start_date,
            'check_out': booking.end_date,
            'room_type': booking.listing.title,
            'total_price': booking.total_price,
            'num_guests': booking.num_guests if hasattr(booking, 'num_guests') else 'N/A',
            'view_booking_url': f"{settings.PUBLIC_URL}/bookings/{booking.booking_id}/",
        }
    )
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=f'Hi {booking.guest.get_full_name()}, your booking is confirmed!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )
    
    email.attach_alternative(html_content, "text/html")
    email.send()
    return f'Email sent to {to_email}'
