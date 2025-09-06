# alx\_travel\_app\_0x03

A Django RESTful API for managing travel listings, bookings, reviews, and payments, enhanced with background tasks for email notifications using Celery and RabbitMQ.

---

## Features

* **User Authentication**: Secure registration and login using Django’s built-in user model and JWT authentication.
* **Listings**: CRUD operations for travel listings (hotels, apartments, experiences).
* **Bookings**: Users can book listings, view their bookings, and manage (change/cancel) them.
* **Reviews**: Users can leave reviews and ratings for listings.
* **Payments**: Integration with Chapa for secure booking payments and verification.
* **Background Tasks**: Asynchronous email notifications for booking confirmations using Celery with RabbitMQ.
* **Permissions**: Fine-grained permissions for viewing, adding, changing, and deleting listings, bookings, reviews, and payments.
* **Browsable API**: Interactive API documentation via Swagger and Redoc.

---

## API Endpoints

All endpoints are prefixed by `/listings/` unless otherwise noted.

| Resource | Endpoint                                   | Methods                 | Description                           |
| -------- | ------------------------------------------ | ----------------------- | ------------------------------------- |
| Listings | `/listings/`                               | GET, POST               | List or create listings               |
| Listings | `/listings/{id}/`                          | GET, PUT, PATCH, DELETE | Retrieve, update, or delete a listing |
| Bookings | `/bookings/`                               | GET, POST               | List or create bookings               |
| Bookings | `/bookings/{id}/`                          | GET, PUT, PATCH, DELETE | Retrieve, update, or delete a booking |
| Reviews  | `/reviews/`                                | GET, POST               | List or create reviews                |
| Reviews  | `/reviews/{id}/`                           | GET, PUT, PATCH, DELETE | Retrieve, update, or delete a review  |
| Payments | `/bookings/{booking_id}/initiate-payment/` | POST                    | Initiate payment via Chapa            |
| Payments | `/bookings/verify-payment/{tx_ref}/`       | GET                     | Verify Chapa payment status           |

> **Note:** Authentication is required for most operations.

---

## Setup & Installation

1. **Clone the repository:**

   ```bash
   git clone <repo-url>
   cd alx_travel_app_0x03
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (admin):**

   ```bash
   python manage.py createsuperuser
   ```

6. **Start RabbitMQ (required for Celery):**

   ```bash
   sudo systemctl start rabbitmq-server
   ```

   or on macOS (Homebrew):

   ```bash
   brew services start rabbitmq
   ```

7. **Start Celery worker:**

   ```bash
   celery -A alx_travel_app worker --loglevel=info
   ```

8. **Run the Django development server:**

   ```bash
   python manage.py runserver
   ```

---

## Email Configuration

Make sure to configure the following in `.env` or `settings.py` for email notifications:

```env
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=your-email@example.com
```

Booking confirmations will be sent asynchronously using Celery.

---

## Project Structure

```
alx_travel_app_0x03/
├── alx_travel_app/
│   ├── listings/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── tasks.py          # Celery tasks (email notifications)
│   │   ├── urls.py
│   │   └── ...
│   ├── celery.py             # Celery app configuration
│   ├── settings.py           # Django settings (with Celery & email)
│   ├── urls.py
│   └── ...
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Background Tasks

* **Celery + RabbitMQ**: Offloads long-running tasks such as sending emails.
* **Booking Email**: `send_booking_email` task sends a confirmation email asynchronously when a booking is created.

Example usage in `BookingViewSet`:

```python
from listings.tasks import send_booking_email

def perform_create(self, serializer):
    booking = serializer.save(guest=self.request.user)
    send_booking_email.delay(booking.guest.email, str(booking.booking_id))
```

---

## Permissions & Roles

Uses Django’s built-in permission system. Example permissions:

* `add_listing`, `change_listing`, `delete_listing`, `view_listing`
* `add_booking`, `change_booking`, `delete_booking`, `view_booking`
* `add_review`, `change_review`, `delete_review`, `view_review`
* `add_payment`, `change_payment`, `view_payment`

---
