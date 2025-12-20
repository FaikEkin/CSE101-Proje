import os
import movies as m_logic
import seating as s_logic
import bookings as b_logic
import storage as st_logic

BASE_DIR = "data"


def admin_menu(movies, showtimes, seat_maps, bookings):
    while True:
        print("\n--- ADMIN PANEL ---")
        print("1. Add Movie\n2. Schedule Showtime\n3. Back")
        choice = input("Choice: ")

        if choice == "1":
            title = input("Title: ")
            m_data = {"id": str(len(movies) + 1), "title": title, "genre": input("Genre: ")}
            m_logic.add_movie(movies, m_data)
            print("Movie added!")
        elif choice == "2":
            sid = input("Showtime ID: ")
            s_data = {"id": sid, "movie_id": input("Movie ID: "), "date": input("Date: ")}
            m_logic.schedule_showtime(showtimes, s_data)
            seat_maps[sid] = s_logic.initialize_seat_map({"rows": 8, "seats_per_row": 12})
            print("Showtime scheduled!")
        elif choice == "3":
            break
        st_logic.save_state(BASE_DIR, movies, showtimes, bookings)


def customer_menu(movies, showtimes, seat_maps, bookings):
    while True:
        print("\n--- CUSTOMER MENU ---")
        print("1. List Showtimes\n2. Book Ticket\n3. Cancel Booking\n4. Back")
        choice = input("Choice: ")

        if choice == "1":
            for s in showtimes: print(f"ID: {s['id']} | Movie: {s['movie_id']} | Date: {s['date']}")
        elif choice == "2":
            sid = input("Enter Showtime ID: ")
            if sid in seat_maps:
                print(s_logic.render_seat_map(seat_maps[sid]))
                seat = input("Select Seat (e.g. A1): ")
                email = input("Email: ")
                # Basit fiyatlandırma örneği
                pricing = {"standard": 100, "premium": 150}
                tier = seat_maps[sid][seat]['tier']
                total = b_logic.calculate_booking_total([tier], pricing, 0.18)

                confirm = input(f"Total: {total['total']}. Confirm? (y/n): ")
                if confirm.lower() == 'y':
                    b_data = {"showtime_id": sid, "seats": [seat], "email": email, "total_price": total['total']}
                    res = b_logic.create_booking(showtimes, seat_maps, b_data)
                    if res:
                        bookings.append(res)
                        print(f"Success! ID: {res['booking_id']}")
            else:
                print("Invalid showtime!")
        elif choice == "3":
            bid = input("Booking ID: ")
            if b_logic.cancel_booking(bookings, bid, seat_maps): print("Cancelled!")
        elif choice == "4":
            break
        st_logic.save_state(BASE_DIR, movies, showtimes, bookings)


def main():
    movies, showtimes, bookings = st_logic.load_state(BASE_DIR)
    # Seat mapler genelde showtime bazlı saklanır, örnek için boş başlıyoruz
    seat_maps = {s['id']: s_logic.initialize_seat_map({}) for s in showtimes}

    while True:
        print("\n=== MOVIE BOOKING SYSTEM ===")
        print("1. Customer\n2. Admin\n3. Exit")
        role = input("Select Role: ")

        if role == "1":
            customer_menu(movies, showtimes, seat_maps, bookings)
        elif role == "2":
            admin_menu(movies, showtimes, seat_maps, bookings)
        elif role == "3":
            break

    st_logic.save_state(BASE_DIR, movies, showtimes, bookings)


if __name__ == "__main__":
    main()