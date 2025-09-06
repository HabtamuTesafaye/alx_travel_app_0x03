from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet, ReviewViewSet, initiate_payment, verify_payment

router = DefaultRouter()
router.register(r'listings', ListingViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('bookings/initiate-payment/<uuid:booking_id>/', initiate_payment, name='initiate-payment'),
    path('bookings/verify-payment/<uuid:tx_ref>/', verify_payment, name='verify-payment'),
]
