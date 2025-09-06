import os
import requests
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django_ratelimit.decorators import ratelimit
from django.conf import settings

from .models import Listing, Booking, Review, Payment
from .serializers import ListingSerializer, BookingSerializer, ReviewSerializer
from listings.tasks import send_booking_email

# Chapa config
CHAPA_SECRET_KEY = os.getenv("CHAPA_SECRET_KEY")
CHAPA_INIT_URL = "https://api.chapa.co/v1/transaction/initialize"
CHAPA_VERIFY_URL = "https://api.chapa.co/v1/transaction/verify/{}"

# ---------- LISTINGS, BOOKINGS, REVIEWS ----------

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        booking = serializer.save(guest=self.request.user)
        
        # Optional: Send email immediately on booking
        send_booking_email.delay(
            to_email=booking.guest.email,
            booking_id=booking.booking_id
        )


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]


# ---------------- PAYMENT ---------------- #

@ratelimit(key='ip', rate='5/m', block=True)
@api_view(['POST'])
@permission_classes([AllowAny])
def initiate_payment(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)

    payload = {
        "amount": str(booking.total_price),
        "currency": "ETB",
        "email": booking.guest.email,
        "tx_ref": str(booking.booking_id),
        "callback_url": f"{settings.PUBLIC_URL}/api/bookings/verify-payment/"
    }

    headers = {"Authorization": f"Bearer {CHAPA_SECRET_KEY}"}

    try:
        response = requests.post(CHAPA_INIT_URL, json=payload, headers=headers)
        data = response.json()
    except Exception as e:
        return JsonResponse({"error": "Payment initiation request failed", "details": str(e)}, status=500)

    if data.get("status") == "success":
        Payment.objects.update_or_create(
            booking=booking,
            defaults={
                "transaction_id": data["data"]["id"],
                "amount": booking.total_price,
                "status": "Pending"
            }
        )
        return JsonResponse({"payment_url": data["data"]["checkout_url"]})

    return JsonResponse({"error": "Payment initiation failed", "details": data}, status=400)


@ratelimit(key='ip', rate='10/m', block=True)
@api_view(['GET'])
@permission_classes([AllowAny])
def verify_payment(request, tx_ref):
    payment = get_object_or_404(Payment, booking__booking_id=tx_ref)
    headers = {"Authorization": f"Bearer {CHAPA_SECRET_KEY}"}

    try:
        response = requests.get(CHAPA_VERIFY_URL.format(tx_ref), headers=headers)
        data = response.json()
    except Exception as e:
        return JsonResponse({"error": "Verification request failed", "details": str(e)}, status=500)

    if data.get("status") == "success":
        status_chapa = data["data"]["status"]
        payment.status = "Completed" if status_chapa == "success" else "Failed"
        if status_chapa == "success":
            payment.booking.status = "confirmed"
            payment.booking.save()
            
            # Send booking confirmation email AFTER successful payment
            send_booking_email.delay(
                to_email=payment.booking.guest.email,
                booking_id=payment.booking.booking_id
            )
        payment.save()
        return JsonResponse({"status": payment.status})

    return JsonResponse({"error": "Payment verification failed", "details": data}, status=400)
