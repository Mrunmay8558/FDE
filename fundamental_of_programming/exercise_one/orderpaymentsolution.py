from fundamental_of_programming.exercise_one.order_payment_exercise import (
    orders,
    payment_details,
    users,
)


def find_user_by_id(user_id):
    for user in users:
        if user["user_id"] == user_id:
            return user

    return None


def find_payment_by_id(payment_id):
    for payment in payment_details:
        if payment["payment_id"] == payment_id:
            return payment

    return None


def find_address_by_id(user, address_id):
    for address in user["addresses"]:
        if address["address_id"] == address_id:
            return address

    return None


def calculate_order_total(order):
    total = 0

    for item in order["items"]:
        item_total = item["quantity"] * item["unit_price"]
        total = total + item_total - item["discount"]

    return total


def get_payment_message(payment):
    if payment["status"] == "SUCCESS":
        return "Payment completed successfully."
    elif payment["status"] == "PENDING":
        return "Payment is pending."
    else:
        return "Payment failed. Do not ship this order."


def get_order_type(order_total):
    if order_total >= 50000:
        return "High Value Order"
    else:
        return "Regular Order"


def get_shipping_decision(order, payment):
    if order["status"] == "CONFIRMED" and payment["status"] == "SUCCESS":
        return "Ready for dispatch"
    else:
        return "Hold order"


def print_order_summary(order):
    user = find_user_by_id(order["user_id"])
    payment = find_payment_by_id(order["payment_id"])
    address = find_address_by_id(user, order["delivery_address_id"])
    order_total = calculate_order_total(order)
    item_names = []

    for item in order["items"]:
        item_names.append(item["name"] + " x " + str(item["quantity"]))

    print("Order ID:", order["order_id"])
    print("Customer:", user["first_name"], user["last_name"])
    print("City:", address["city"])
    print("Payment Method:", payment["method"])
    print("Payment Status:", payment["status"])
    print("Payment Message:", get_payment_message(payment))
    print("Order Total:", order_total, payment["currency"])
    print("Order Type:", get_order_type(order_total))
    print("Shipping Decision:", get_shipping_decision(order, payment))
    print("Items:", ", ".join(item_names))
    print("-" * 40)


print("ALL ORDER SUMMARIES")
print("-" * 40)

for order in orders:
    print_order_summary(order)


# Bonus 1: Print only orders where the linked payment status is SUCCESS.
print("SUCCESSFUL ORDERS ONLY")
print("-" * 40)

for order in orders:
    payment = find_payment_by_id(order["payment_id"])

    if payment["status"] == "SUCCESS":
        print_order_summary(order)


# Bonus 2: Count how many orders each user has placed.
print("ORDERS PLACED BY EACH USER")
print("-" * 40)

for user in users:
    order_count = 0

    for order in orders:
        if order["user_id"] == user["user_id"]:
            order_count = order_count + 1

    print(user["first_name"], user["last_name"], "placed", order_count, "orders")

print("-" * 40)


# Bonus 3: Find and print the highest value order.
highest_value_order = orders[0]
highest_order_total = calculate_order_total(highest_value_order)

for order in orders:
    order_total = calculate_order_total(order)

    if order_total > highest_order_total:
        highest_value_order = order
        highest_order_total = order_total

print("HIGHEST VALUE ORDER")
print("-" * 40)
print_order_summary(highest_value_order)
