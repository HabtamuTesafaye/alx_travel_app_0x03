from rest_framework import serializers
from .models import Listing, Booking, Review

class ListingSerializer(serializers.ModelSerializer):
    price_display = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = ['listing_id', 'title', 'description', 'location', 'price_per_night', 'price_display']

    def get_price_display(self, obj):
        return f"${obj.price_per_night:.2f} per night"

class BookingSerializer(serializers.ModelSerializer):
    guest_email = serializers.CharField(source='guest.email', read_only=True)
    listing_title = serializers.CharField(source='listing.title', read_only=True)

    class Meta:
        model = Booking
        fields = ['booking_id', 'guest', 'guest_email', 'listing', 'listing_title', 'start_date', 'end_date', 'total_price', 'status', 'created_at']
        read_only_fields = ['booking_id', 'created_at']

    def validate(self, data):
        if data['end_date'] <= data['start_date']:
            raise serializers.ValidationError("End date must be after start date.")
        return data

class ReviewSerializer(serializers.ModelSerializer):
    reviewer_email = serializers.CharField(source='reviewer.email', read_only=True)
    listing_title = serializers.CharField(source='listing.title', read_only=True)

    class Meta:
        model = Review
        fields = ['review_id', 'reviewer', 'reviewer_email', 'listing', 'listing_title', 'rating', 'comment', 'created_at']
        read_only_fields = ['review_id', 'created_at']

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
