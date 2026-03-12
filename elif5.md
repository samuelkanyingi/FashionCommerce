# FashionHub E-Commerce Project Documentation

## Overview

FashionHub is a Django-based e-commerce platform for selling fashion products (clothing, shoes, accessories) for men and women. The system supports guest checkout, M-Pesa payment integration, order tracking, and PDF receipt generation.

---

## Project Structure

```
FashionV3/
├── shop/                      # Main Django app
│   ├── models.py             # Database models
│   ├── views.py              # Business logic
│   ├── urls.py               # URL routing
│   ├── migrations/           # Database migrations
│   └── utils/
│       └── mpesa.py          # M-Pesa API utilities
├── templates/shop/            # HTML templates
│   ├── base.html             # Base template with navbar/footer
│   ├── index.html            # Homepage
│   ├── women.html            # Women's products page
│   ├── men.html              # Men's products page
│   ├── cart.html             # Shopping cart page
│   ├── product_detail.html   # Product details page
│   ├── track_order.html      # Order tracking page
│   └── ...
├── fashion_project/          # Django project settings
│   ├── settings.py           # Configuration
│   └── urls.py               # Project URLs
└── static/                   # Static files (CSS, JS, images)
```

---

## Database Models

### 1. Product
Represents items for sale.

```
Fields:
- id: Auto-increment primary key
- name: Product name
- description: Product details
- price: Price in KES
- image: Product photo (uploaded to media/products/)
- category: "women" or "men"
- subcategory: e.g., "shoes", "clothing", "handbags"
- stock: Available quantity
```

### 2. Order
Represents a customer order.

```
Fields:
- id: Auto-increment primary key
- buyer: ForeignKey to User (nullable for guest checkout)
- tracking_number: Unique 8-char identifier (auto-generated UUID)
- status: "PENDING" or "PAID"
- phone: Customer phone number
- email: Customer email
- location: Delivery location (from OpenStreetMap)
- address: Delivery address
- landmark: Nearby landmark
- delivery_fee: Delivery cost
- mpesa_receipt: M-Pesa transaction receipt number
- created_at: Order creation timestamp
- checkout_request_id: M-Pesa STK push request ID

Methods:
- get_total_amount(): Sum of all OrderItem totals
- get_grand_total(): Total + delivery fee
```

### 3. OrderItem
Individual items within an order.

```
Fields:
- id: Auto-increment primary key
- order: ForeignKey to Order
- product: ForeignKey to Product
- quantity: Number of items
- price: Price at time of purchase
- size: Selected size (S/M/L/XL or shoe sizes)
```

### 4. Receipt
PDF receipt for paid orders.

```
Fields:
- id: Auto-increment primary key
- order: OneToOneField to Order
- receipt_number: Unique receipt ID (e.g., "RCP-ABC12345")
- generated_at: Creation timestamp
- pdf_file: Binary PDF content
```

### 5. Review
Customer product reviews.

```
Fields:
- id: Auto-increment primary key
- product: ForeignKey to Product
- name: Reviewer name
- rating: 1-5 star rating
- comment: Review text
- created_at: Submission timestamp
```

### 6. Report
Stored analytics reports.

```
Fields:
- id: Auto-increment primary key
- report_type: Type of report (sales, inventory, etc.)
- title: Report title
- generated_at: Creation timestamp
- data: JSON data containing report metrics
```

---

## URL Routes

| URL | View Function | Description |
|-----|---------------|-------------|
| `/` | `index` | Homepage |
| `/women` | `women` | Women's products |
| `/men` | `men` | Men's products |
| `/search/` | `search` | Product search |
| `/product/<id>/` | `product_detail` | Product details page |
| `/product/<id>/review/` | `submit_review` | Submit product review |
| `/cart` | `cart` | Shopping cart |
| `/add_to_cart` | `add_to_cart` | Add item to cart (AJAX) |
| `/update_cart` | `update_cart` | Update quantity (AJAX) |
| `/remove_item` | `remove_item` | Remove item (AJAX) |
| `/mpesa/stk/<id>/` | `stk_push` | Initiate M-Pesa payment |
| `/mpesa/callback/` | `mpesa_callback` | M-Pesa payment callback |
| `/check-order-status/` | `check_order_status` | Check payment status (AJAX) |
| `/track-order/` | `track_order` | Track order by tracking number/email |
| `/inventory/` | `inventory` | Admin inventory management |
| `/reports/` | `reports` | Sales reports dashboard |
| `/receipt/<id>/` | `receipt` | View order receipt |
| `/my-receipts/` | `my_receipts` | List user's receipts |

---

## How the Shopping Flow Works

### Step 1: Browse Products
1. User visits `/women` or `/men` page
2. Products displayed in a grid from database
3. User can filter by subcategory (clothing, shoes, handbags)
4. User can sort by price (high-to-low, low-to-high)

### Step 2: View Product Details
1. User clicks product image
2. Navigates to `/product/<id>/`
3. Shows: large image, name, price, size selector, description
4. Shows reviews and rating
5. User can write reviews (Alpine.js form)

### Step 3: Add to Cart
1. User clicks "Add to Cart" button
2. Form submits via HTMX to `/add_to_cart`
3. View adds item to session cart:
   ```python
   cart = request.session.get("cart", [])
   # Add product info: name, price, image, quantity, size
   request.session["cart"] = cart
   ```
4. Cart icon updates with item count
5. User redirected to cart page

### Step 4: Manage Cart
1. User visits `/cart`
2. Cart displays all items from session
3. User can:
   - Increase/decrease quantity (via HTMX)
   - Remove items
   - See order summary with subtotal

### Step 5: Checkout
1. User clicks "Proceed to Checkout"
2. Checkout sidebar opens (Alpine.js)
3. **Step 1 - Location:**
   - User enters delivery location
   - Google Maps/OpenStreetMap calculates distance
   - Delivery fee calculated: distance × KES 10
   - Free delivery for orders over KES 20,000
4. **Step 2 - Payment:**
   - User enters M-Pesa phone number
   - Form submits to `/mpesa/stk/<order_id>/`
5. **Step 3 - Review:**
   - Shows order summary
   - User clicks "Confirm & Pay"

### Step 6: M-Pesa Payment
1. `/stk_push` view:
   - Gets M-Pesa access token
   - Sends STK push to M-Pesa API
   - Returns success message to user
2. User receives M-Pesa prompt on phone
3. User enters PIN to pay
4. M-Pesa sends callback to `/mpesa/callback/`

### Step 7: Payment Confirmation
1. `/mpesa_callback` receives payment confirmation:
   - Updates order status to "PAID"
   - Saves M-Pesa receipt number
   - Generates PDF receipt
   - Sends email with receipt
2. When user visits cart next time:
   - System detects PAID order from last 10 minutes
   - Cart is automatically cleared

### Step 8: Order Tracking
1. User visits `/track-order/`
2. Enters tracking number OR email
3. System finds matching PAID order
4. Shows order status, items, delivery info

---

## Session-Based Cart System

The cart uses Django sessions to store items:

```python
# Session structure
request.session["cart"] = [
    {
        "product_id": "1",
        "name": "Midi Dress",
        "price": 2000,
        "image": "/media/products/dress.jpg",
        "quantity": 2,
        "size": "M",
        "description": "..."
    },
    ...
]

# For guest users
request.session["guest_order_id"] = 123
```

**Benefits:**
- No account required for guests
- Cart persists across page loads
- Works with Django's session framework

---

## M-Pesa Integration

### STK Push Flow
1. User initiates payment
2. Backend calls M-Pesa API with:
   - Business Short Code: 174379
   - Amount: Order total
   - Phone: Customer number
   - CallBackURL: Your ngrok/render URL
3. M-Pesa sends push to user's phone
4. User enters PIN
5. M-Pesa calls your callback URL with result

### Configuration
- Uses Safaricom Daraja API (sandbox)
- Credentials stored in environment variables
- Token-based authentication

---

## Guest Checkout

The system supports checkout without login:

1. **Nullable buyer field:** `buyer = ForeignKey(User, null=True, blank=True)`
2. **Session-based order:** `guest_order_id` stored in session
3. **Email required:** Must provide email for receipt
4. **Order tracking:** Via tracking number or email

---

## Template Technologies

### HTML/CSS
- Bootstrap-like custom CSS
- Responsive design
- Custom styling for product cards, cart, checkout

### JavaScript
- **Alpine.js:** For interactive UI (checkout sidebar, quantity controls, reviews)
- **HTMX:** For AJAX requests (add to cart, update quantity, remove item)
- **Google Maps API:** For location selection
- **OpenStreetMap:** For distance calculation

---

## Key Features

1. **Product Catalog**
   - Categories: Women, Men
   - Subcategories: Clothing, Shoes, Handbags, Watches
   - Product images
   - Stock management

2. **Shopping Cart**
   - Session-based (guest-friendly)
   - Size selection
   - Quantity adjustment
   - Real-time total calculation

3. **Checkout**
   - Location-based delivery fee
   - M-Pesa STK push payment
   - Order confirmation

4. **Order Management**
   - Automatic order creation
   - Order status tracking (PENDING → PAID)
   - PDF receipt generation
   - Email delivery

5. **Order Tracking**
   - By tracking number
   - By email address
   - Guest-friendly

6. **Product Reviews**
   - Star ratings (1-5)
   - Comment text
   - Shows on product detail page

7. **Reports Dashboard**
   - Sales reports
   - Inventory status
   - Order analytics

---

## Admin Features

- `/inventory/` - Manage product stock
- `/reports/` - View sales reports
- `/my-receipts/` - View order receipts
- Django admin panel for full CRUD

---

## Environment Variables

Key settings in `fashion_project/settings.py`:

```
DEBUG=True/False
SECRET_KEY=...
DATABASE_URL=...
EMAIL_HOST_USER=...
MPESA_CONSUMER_KEY=...
MPESA_CONSUMER_SECRET=...
MPESA_SHORTCODE=...
MPESA_PASSKEY=...
GOOGLE_MAPS_API_KEY=...
```

---

## Running the Project

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Run development server
python manage.py runserver

# For production (Render)
gunicorn fashion_project.wsgi
```

---

## Future Enhancements

1. User accounts with order history
2. Multiple payment methods
3. Inventory alerts (low stock)
4. Email notifications
5. Order delivery tracking
6. Product search filters
7. Wishlist functionality
8. Coupon/discount codes
