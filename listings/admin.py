from django.contrib import admin
from .models import Listing, Booking, Review, Payment

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'host_email', 'price_per_night', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'location', 'host__email')
    list_filter = ('created_at', 'updated_at')

    def host_email(self, obj):
        return obj.host.email
    host_email.short_description = 'Host Email'

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'listing_title', 'guest_email', 'start_date', 'end_date', 'total_price', 'status', 'created_at')
    search_fields = ('listing__title', 'guest__email', 'booking_id')
    list_filter = ('status', 'created_at')
    list_select_related = ('guest', 'listing')

    def guest_email(self, obj):
        return obj.guest.email
    guest_email.short_description = 'Guest Email'

    def listing_title(self, obj):
        return obj.listing.title
    listing_title.short_description = 'Listing'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'listing_title', 'reviewer_email', 'rating', 'created_at')
    search_fields = ('listing__title', 'reviewer__email')
    list_filter = ('rating', 'created_at')

    def reviewer_email(self, obj):
        return obj.reviewer.email
    reviewer_email.short_description = 'Reviewer Email'

    def listing_title(self, obj):
        return obj.listing.title
    listing_title.short_description = 'Listing'

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'booking_id', 'amount', 'status', 'created_at', 'updated_at')
    search_fields = ('transaction_id', 'booking__booking_id')
    list_filter = ('status', 'created_at', 'updated_at')

    def booking_id(self, obj):
        return obj.booking.booking_id
    booking_id.short_description = 'Booking ID'
