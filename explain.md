# FashionHub - Detailed Project Documentation

FashionHub is a modern, robust E-commerce platform built with a focus on performance, real-time interactivity, and secure payment processing.

## 1. The Core Architecture
FashionHub follows a "Low-JS" philosophy to provide a snappy, app-like experience without the overhead of heavy frontend frameworks:
*   **Django (Backend):** Serves as the backbone, handling database management (PostgreSQL), business logic, user security, and server-side rendering.
*   **HTMX (Dynamic UI):** Powers the "no-refresh" feel. It allows the cart, search results, and checkout updates to happen instantly by swapping HTML fragments.
*   **Alpine.js (Interactivity):** Manages client-side states, such as the sliding promotion carousel, the Quick View sidebar, and real-time form validations.
*   **ReportLab:** Dynamically generates professional, branded PDF receipts for every successful transaction.

## 2. The Shopping Lifecycle
### A. Browsing & Product Selection
*   **Dynamic Grid:** Products are fetched and filtered in real-time by category (Men/Women) or subcategory.
*   **Quick View Sidebar:** Users can view product details and select sizes without leaving the gallery. Size selection is strictly enforced via Alpine.js before adding to cart.
*   **Search Engine:** Uses a broad `icontains` database filter to provide accurate results across the entire catalog.

### B. Intelligent Cart Management
*   **Dual-Layer Sync:** The system maintains a temporary session-based cart for speed, while automatically synchronizing it with `Order` and `OrderItem` records in the database for persistence.
*   **Live Updates:** Quantities and deletions update the header cart count and subtotal instantly using HTMX "Out-of-Band" (OOB) swaps.

### C. Advanced Checkout Flow
*   **Step 1: Shipping:** Captures location and contact data. The `update_shipping` route saves progress immediately to prevent data loss.
*   **Step 2: Payment:** Seamless integration with Safaricom M-Pesa.
*   **Step 3: Review:** Provides a final, transparent breakdown of items, automated delivery fee calculation based on location, and the grand total.

## 3. Payment & Inventory Accuracy
### M-Pesa Integration
*   **STK Push:** Initiates a secure payment request directly to the user's phone.
*   **Asynchronous Callback:** Uses a unique `CheckoutRequestID` to verify payments. Once successful, the order status moves to `PAID`.
*   **Automated Stock Management:** The moment a payment is confirmed, the system automatically decrements the stock levels for all purchased items.

### Professional Fulfillment
*   **Unified Receipts:** Successful payments trigger a three-way fulfillment:
    1.  An on-platform success page.
    2.  A branded HTML confirmation email.
    3.  A professionally styled PDF attachment matching the platform's aesthetic.

## 4. Admin Intelligence (Reporting Dashboard)
The admin area provides real-time business insights, recalculating data every time the page is refreshed:
1.  **Sales Summary:** Tracks total revenue and successful transaction history.
2.  **Stock Alert:** Identifies items falling below the "Low Stock" threshold (10 units).
3.  **Order Status:** Analyzes the ratio of Paid vs. Pending orders.
4.  **Customer Leaders:** Ranks users by order volume and successful payments.
5.  **Product Performance:** Monitors satisfaction through customer ratings and reviews.
6.  **Best Sellers:** Identifies the top 30 most frequently ordered items.

## 5. User Account Features
*   **Order History:** A dedicated dashboard for users to track paid orders or cancel unwanted pending ones.
*   **Secure Authentication:** Includes a professional password recovery flow using signed tokens and modern HTML email templates.

---
*Documented on March 12, 2026*
