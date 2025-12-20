import os


def occupancy_report(showtimes, seat_maps, bookings):
    report = {}
    for st in showtimes:
        sid = st['id']
        s_map = seat_maps.get(sid, {})
        total_seats = len(s_map)
        sold_seats = sum(1 for s in s_map.values() if s['status'] == 'sold')
        rate = (sold_seats / total_seats * 100) if total_seats > 0 else 0
        report[sid] = {
            "movie": st['movie_id'],
            "sold": sold_seats,
            "rate": f"{rate:.2f}%"
        }
    return report


def revenue_summary(bookings, period=None):
    total = 0
    confirmed_bookings = [b for b in bookings if b['status'] == 'confirmed']

    if period:
        start, end = period
        confirmed_bookings = [b for b in confirmed_bookings if start <= b['created_at'] <= end]

    for b in confirmed_bookings:
        total += b['total_price']

    return {"total_revenue": round(total, 2), "count": len(confirmed_bookings)}


def top_movies(bookings, showtimes, limit=5):
    movie_counts = {}
    confirmed = [b for b in bookings if b['status'] == 'confirmed']

    for b in confirmed:
        st = next((s for s in showtimes if s['id'] == b['showtime_id']), None)
        if st:
            m_id = st['movie_id']
            movie_counts[m_id] = movie_counts.get(m_id, 0) + 1

    sorted_movies = sorted(movie_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_movies[:limit]


def export_report(report_data, filename):
    directory = "reports_export"
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)

    with open(path, 'w') as f:
        for key, val in report_data.items():
            f.write(f"{key}: {val}\n")
    return path