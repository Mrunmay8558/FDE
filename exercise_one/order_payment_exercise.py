"""
Exercise One: Users, Orders, And Payment Details

Goal:
You are given three collections:
1. users: customer profile and address details
2. payment_details: payment records created separately
3. orders: order records that store only the payment_id, not the full payment object

Your task is to connect these records together and print a clean order summary.
"""

# Payment records are stored separately. Each order will only keep the payment_id.
payment_details = [
    {
        "payment_id": "PAY-1001",
        "method": "UPI",
        "provider": "Google Pay",
        "status": "SUCCESS",
        "amount_paid": 84999,
        "currency": "INR",
        "transaction_reference": "TXN-GPAY-908811",
    },
    {
        "payment_id": "PAY-1002",
        "method": "Credit Card",
        "provider": "HDFC Bank",
        "status": "PENDING",
        "amount_paid": 4598,
        "currency": "INR",
        "transaction_reference": "TXN-HDFC-773401",
    },
    {
        "payment_id": "PAY-1003",
        "method": "Wallet",
        "provider": "Amazon Pay",
        "status": "FAILED",
        "amount_paid": 0,
        "currency": "INR",
        "transaction_reference": "TXN-AMZ-332019",
    },
]


# User records contain personal information and multiple address details.
users = [
    {
        "user_id": "USR-501",
        "first_name": "Aarav",
        "last_name": "Mehta",
        "email": "aarav.mehta@example.com",
        "phone": "+91-9876543210",
        "addresses": [
            {
                "address_id": "ADDR-01",
                "type": "home",
                "line_1": "42 Palm Residency",
                "line_2": "Near City Mall",
                "city": "Mumbai",
                "state": "Maharashtra",
                "pincode": 400001,
                "is_primary": True,
            },
            {
                "address_id": "ADDR-02",
                "type": "office",
                "line_1": "14th Floor, Solaris Tower",
                "line_2": "Andheri East",
                "city": "Mumbai",
                "state": "Maharashtra",
                "pincode": 400069,
                "is_primary": False,
            },
        ],
    },
    {
        "user_id": "USR-502",
        "first_name": "Nisha",
        "last_name": "Rao",
        "email": "nisha.rao@example.com",
        "phone": "+91-9123456780",
        "addresses": [
            {
                "address_id": "ADDR-03",
                "type": "home",
                "line_1": "88 Green Avenue",
                "line_2": "Koramangala",
                "city": "Bengaluru",
                "state": "Karnataka",
                "pincode": 560034,
                "is_primary": True,
            }
        ],
    },
]


# Orders are complex items. Notice that each order stores user_id and payment_id only.
# The full user and full payment information must be found from users and payment_details.
orders = [
    {
        "order_id": "ORD-9001",
        "user_id": "USR-501",
        "payment_id": "PAY-1001",
        "status": "CONFIRMED",
        "delivery_address_id": "ADDR-01",
        "items": [
            {
                "product_id": "PRD-701",
                "name": "Gaming Laptop",
                "category": "Electronics",
                "quantity": 1,
                "unit_price": 84999,
                "discount": 5000,
            }
        ],
    },
    {
        "order_id": "ORD-9002",
        "user_id": "USR-502",
        "payment_id": "PAY-1002",
        "status": "AWAITING_PAYMENT",
        "delivery_address_id": "ADDR-03",
        "items": [
            {
                "product_id": "PRD-812",
                "name": "Bluetooth Keyboard",
                "category": "Accessories",
                "quantity": 1,
                "unit_price": 2499,
                "discount": 200,
            },
            {
                "product_id": "PRD-813",
                "name": "Wireless Mouse",
                "category": "Accessories",
                "quantity": 1,
                "unit_price": 2299,
                "discount": 0,
            },
        ],
    },
    {
        "order_id": "ORD-9003",
        "user_id": "USR-501",
        "payment_id": "PAY-1003",
        "status": "PAYMENT_FAILED",
        "delivery_address_id": "ADDR-02",
        "items": [
            {
                "product_id": "PRD-610",
                "name": "Office Chair",
                "category": "Furniture",
                "quantity": 1,
                "unit_price": 12999,
                "discount": 1500,
            },
            {
                "product_id": "PRD-611",
                "name": "Laptop Stand",
                "category": "Furniture",
                "quantity": 2,
                "unit_price": 1499,
                "discount": 100,
            },
        ],
    },
]


"""
Question: Build An Order And Payment Summary System

You are working on a small e-commerce system. The company stores users,
orders, and payment details in separate lists. The order does not store the
full user object or full payment object. It only stores user_id, payment_id,
and delivery_address_id.

Your job is to join this information manually and print a readable summary for
each order.

Main Requirements:

1. Loop through the orders list.
2. For each order, find the matching user using user_id.
3. For each order, find the matching payment using payment_id.
4. For each order, find the matching delivery address using delivery_address_id.
5. Calculate the total order amount:
    total = sum of (quantity * unit_price) minus all item discounts
6. Use an if/elif/else statement for payment status:
    - If payment status is SUCCESS, print: Payment completed successfully.
    - If payment status is PENDING, print: Payment is pending.
    - Otherwise, print: Payment failed. Do not ship this order.
7. Use an if/else statement for order value:
    - If order total is greater than or equal to 50000, print: High Value Order
    - Otherwise, print: Regular Order
8. Use an if/else statement for shipping decision:
    - If order status is CONFIRMED and payment status is SUCCESS, print: Ready for dispatch
    - Otherwise, print: Hold order

Expected Output Format:

Order ID: ORD-9001
Customer: Aarav Mehta
City: Mumbai
Payment Method: UPI
Payment Status: SUCCESS
Payment Message: Payment completed successfully.
Order Total: 79999 INR
Order Type: High Value Order
Shipping Decision: Ready for dispatch
Items: Gaming Laptop x 1
----------------------------------------

Bonus Challenge:

1. Print only successful orders.
2. Print how many orders each user has placed.
3. Print the highest value order.
"""


# Write your solution below this line.
# Do not change the data above. Use loops, conditions, dictionaries, and list access.
