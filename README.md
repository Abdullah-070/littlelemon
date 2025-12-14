# Little Lemon Restaurant - Booking Application

A Django-based restaurant table booking application with REST API support, MySQL database integration, and a responsive web interface.

## Features

- ✓ Table booking system with date and time slot selection
- ✓ Dynamic slot availability based on existing bookings
- ✓ Professional UI with responsive design
- ✓ MySQL database integration
- ✓ REST API endpoints for Menu and Bookings management
- ✓ User authentication with token-based API access
- ✓ Success modal confirmation after booking
- ✓ Reservations display page with detailed booking information


## API Endpoints

### Base URL
```
http://127.0.0.1:8000/
```

### Authentication
Most API endpoints require token-based authentication. Include the token in the header:
```
Authorization: Token YOUR_TOKEN_HERE
```

---

## User & Authentication Endpoints

### 1. User Registration (Public)
**POST** `/api/register/`

Register a new user account.

**Request Body:**
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password123"
}
```

**Response:**
```json
{
    "message": "User created successfully"
}
```

---

### 2. Get Authentication Token (Public)
**POST** `/api/token/`

Obtain an authentication token using credentials.

**Request Body:**
```json
{
    "username": "john_doe",
    "password": "secure_password123"
}
```

**Response:**
```json
{
    "token": "abc123xyz789..."
}
```

---

## Menu API Endpoints

### 3. List All Menu Items
**GET** `/api/menu/`

Retrieve all menu items. Requires authentication.

**Response:**
```json
[
    {
        "id": 1,
        "title": "Pasta Carbonara",
        "price": "12.99",
        "inventory": 50
    },
    {
        "id": 2,
        "title": "Grilled Fish",
        "price": "18.50",
        "inventory": 30
    }
]
```

---

### 4. Create Menu Item
**POST** `/api/menu/`

Add a new menu item. Requires authentication.

**Request Body:**
```json
{
    "title": "Risotto",
    "price": "14.99",
    "inventory": 40
}
```

**Response:**
```json
{
    "id": 3,
    "title": "Risotto",
    "price": "14.99",
    "inventory": 40
}
```

---

### 5. Get Menu Item Details
**GET** `/api/menu/{id}/`

Retrieve a specific menu item. Requires authentication.

**Response:**
```json
{
    "id": 1,
    "title": "Pasta Carbonara",
    "price": "12.99",
    "inventory": 50
}
```

---

### 6. Update Menu Item
**PUT** `/api/menu/{id}/`

Update a menu item. Requires authentication.

**Request Body:**
```json
{
    "title": "Pasta Carbonara",
    "price": "13.99",
    "inventory": 45
}
```

---

### 7. Delete Menu Item
**DELETE** `/api/menu/{id}/`

Delete a menu item. Requires authentication.

---

## Table Booking API Endpoints

### 8. List All Bookings
**GET** `/api/bookings/`

Retrieve all table bookings. Requires authentication.

**Response:**
```json
[
    {
        "id": 1,
        "first_name": "Abdullah",
        "reservation_date": "2025-12-23",
        "reservation_slot": 10
    },
    {
        "id": 2,
        "first_name": "Ahmed",
        "reservation_date": "2025-12-24",
        "reservation_slot": 14
    }
]
```

---

### 9. Create a Booking
**POST** `/api/bookings/`

Create a new table booking. Requires authentication.

**Request Body:**
```json
{
    "first_name": "Hassan",
    "reservation_date": "2025-12-25",
    "reservation_slot": 18
}
```

**Response:**
```json
{
    "id": 3,
    "first_name": "Hassan",
    "reservation_date": "2025-12-25",
    "reservation_slot": 18
}
```

---

### 10. Get Booking Details
**GET** `/api/bookings/{id}/`

Retrieve details of a specific booking. Requires authentication.

**Response:**
```json
{
    "id": 1,
    "first_name": "Abdullah",
    "reservation_date": "2025-12-23",
    "reservation_slot": 10
}
```

---

### 11. Update Booking
**PUT** `/api/bookings/{id}/`

Update a booking. Requires authentication.

**Request Body:**
```json
{
    "first_name": "Abdullah",
    "reservation_date": "2025-12-25",
    "reservation_slot": 15
}
```

---

### 12. Delete Booking
**DELETE** `/api/bookings/{id}/`

Delete a booking. Requires authentication.

---

## Booking Availability API

### 13. Get Booked Slots for a Date (Public)
**GET** `/api/booked-slots/?date=YYYY-MM-DD`

Retrieve all booked time slots for a specific date. This endpoint is public (no authentication required).

**Query Parameters:**
- `date` (required): Date in YYYY-MM-DD format

**Example:**
```
GET /api/booked-slots/?date=2025-12-23
```

**Response:**
```json
{
    "date": "2025-12-23",
    "booked_slots": [10, 11, 14],
    "available_slots": [12, 13, 15, 16, 17, 18, 19, 20]
}
```

---

## Web Pages

### 14. Home Page
**GET** `/`

Landing page with welcome message.

---

### 15. About Page
**GET** `/about/`

Restaurant information page.

---

### 16. Book a Table Page
**GET** `/book/`

Interactive table booking form with:
- First name input
- Date picker (calendar opens on click)
- Time slot selector (dynamic - disables booked slots)
- Success modal on submission

**POST** `/book/`

Submit a table booking through the web form.

---

### 17. View Reservations Page
**GET** `/reservations/`

Display all current reservations in a formatted table with columns:
- ID
- First Name
- Reservation Date
- Time Slot

---


## Testing API with cURL

### Get Authentication Token
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john_doe","password":"password123"}'
```

### List Menu Items (with token)
```bash
curl -X GET http://127.0.0.1:8000/api/menu/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Get Booked Slots (public - no token needed)
```bash
curl -X GET "http://127.0.0.1:8000/api/booked-slots/?date=2025-12-23"
```

### Create a Booking (with token)
```bash
curl -X POST http://127.0.0.1:8000/api/bookings/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name":"Hassan",
    "reservation_date":"2025-12-25",
    "reservation_slot":18
  }'
```
