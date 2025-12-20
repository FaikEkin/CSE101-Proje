import uuid
from datetime import datetime, timedelta


def calculate_booking_total(seats, pricing, tax_rate, discounts=None):
    subtotal = 0
    for seat_tier in seats:
        subtotal += pricing.get(seat_tier, 0)

    discount_val = 0
    if discounts:
        for d in discounts:
            discount_val += subtotal * d.get('rate', 0)

    net_total = subtotal - discount_val
    tax = net_total * tax_rate

    return {
        "subtotal": round(subtotal, 2),
        "discount": round(discount_val, 2),
        "tax": round(tax, 2),
        "total": round(net_total + tax, 2)
    }


def create_booking(showtimes, seat_maps, booking_data):
    sid = booking_data['showtime_id']
    target_seats = booking_data['seats']
    s_map = seat_maps[sid]

    for code in target_seats:
        if s_map[code]['status'] != 'available':
            return {}

    for code in target_seats:
        s_map[code]['status'] = 'sold'

    b_id = str(uuid.uuid4())[:8].upper()
    new_booking = {
        "booking_id": b_id,
        "showtime_id": sid,
        "customer_email": booking_data['email'],
        "seats": target_seats,
        "total_price": booking_data['total_price'],
        "status": "confirmed",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    return new_booking


def cancel_booking(bookings, booking_id, seat_maps):
    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if not booking:
        return False

    sid = booking['showtime_id']
    for code in booking['seats']:
        seat_maps[sid][code]['status'] = 'available'

    booking['status'] = 'cancelled'
    return True


def list_customer_bookings(bookings, email):
    return [b for b in bookings if b['customer_email'] == email]


def generate_ticket(booking, directory):
    import os
    os.makedirs(directory, exist_ok=True)
    fname = f"ticket_{booking['booking_id']}.txt"
    path = os.path.join(directory, fname)

    content = f"--- TICKET ---\nID: {booking['booking_id']}\nSEATS: {', '.join(booking['seats'])}\nTOTAL: {booking['total_price']}"
    with open(path, 'w') as f:
        f.write(content)
    return path