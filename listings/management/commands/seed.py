from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Listing, Booking, Review
from datetime import date, timedelta

class Command(BaseCommand):
    help = "Seed database with listings, bookings, and reviews"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        users = {
            "emma@example.com": User.objects.get_or_create(email="emma@example.com", defaults={"username": "emma"})[0],
            "liam@example.com": User.objects.get_or_create(email="liam@example.com", defaults={"username": "liam"})[0],
            "olivia@example.com": User.objects.get_or_create(email="olivia@example.com", defaults={"username": "olivia"})[0],
            "noah@example.com": User.objects.get_or_create(email="noah@example.com", defaults={"username": "noah"})[0],
        }

        listings_data = [
            {"title": "Seaside Retreat", "host_email": "emma@example.com", "price_per_night": 120, "location": "Bahirdar", "description": "Nice seaside stay"},
            {"title": "Mountain Cabin", "host_email": "liam@example.com", "price_per_night": 95, "location": "Entoto", "description": "Cozy mountain cabin"},
            {"title": "City Apartment", "host_email": "olivia@example.com", "price_per_night": 150, "location": "Addis Ababa", "description": "Modern city apartment"},
        ]

        listings = {}

        for data in listings_data:
            host = users[data["host_email"]]
            listing, created = Listing.objects.get_or_create(
                title=data["title"],
                host=host,
                defaults={
                    "price_per_night": data["price_per_night"],
                    "location": data["location"],
                    "description": data["description"],
                }
            )
            listings[data["title"]] = listing
            self.stdout.write(f"{'Created' if created else 'Exists'} listing: {listing.title}")

        bookings_data = [
            {"property_title": "Seaside Retreat", "guest_email": "liam@example.com", "nights": 3},
            {"property_title": "Mountain Cabin", "guest_email": "olivia@example.com", "nights": 2},
            {"property_title": "City Apartment", "guest_email": "noah@example.com", "nights": 5},
        ]

        for b in bookings_data:
            listing = listings[b["property_title"]]
            guest = users[b["guest_email"]]
            start_date = date.today() + timedelta(days=1)
            end_date = start_date + timedelta(days=b["nights"])
            total_price = listing.price_per_night * b["nights"]
            booking, created = Booking.objects.get_or_create(
                listing=listing,
                guest=guest,
                start_date=start_date,
                end_date=end_date,
                total_price=total_price,
                status='confirmed'
            )
            self.stdout.write(f"{'Created' if created else 'Exists'} booking at {listing.title} for {guest.email}")

        reviews_data = [
            {"property_title": "Seaside Retreat", "reviewer_email": "liam@example.com", "rating": 5, "comment": "Fantastic!"},
            {"property_title": "Mountain Cabin", "reviewer_email": "olivia@example.com", "rating": 4, "comment": "Very cozy."},
            {"property_title": "City Apartment", "reviewer_email": "noah@example.com", "rating": 3, "comment": "Decent stay."},
        ]

        for r in reviews_data:
            listing = listings[r["property_title"]]
            reviewer = users[r["reviewer_email"]]
            review, created = Review.objects.get_or_create(
                listing=listing,
                reviewer=reviewer,
                rating=r["rating"],
                comment=r["comment"]
            )
            self.stdout.write(f"{'Created' if created else 'Exists'} review for {listing.title} by {reviewer.email}")

        self.stdout.write(self.style.SUCCESS("Seeding complete (Listings, Bookings, Reviews only)!"))
