import razorpay
from django.conf import settings

def initiate_razorpay_payment(product):
    amount = int(product.max_price * 100)  # Convert the amount to paise
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

    payment_order = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
    order_id = payment_order['id']

    # Additional logic to save the order_id and other details to your database

    payment_data = {
        'order_id': order_id,
        'amount': amount,
        'product_name': product.name,
        # Add other necessary data
    }

    return payment_data