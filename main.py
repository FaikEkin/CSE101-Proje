import os
import movies as m_logic
import seating as s_logic
import bookings as b_logic
import storage as st_logic

BASE_DIR = "data"

def get_movie_title(movies, movie_id):
    for movie in movies:
        if str(movie['id']) == str(movie_id):
            return movie['title']
    return "Unknown Movie"

def admin_menu(movies, showtimes, seat_maps, bookings):
    while True:
        print("\n--- ADMIN PANEL ---")
        print("1. Add Movie\n2. Schedule Showtime\n3. Back")
        choice = input("Selection: ")
        
        if choice == "1":
            title = input("Movie Title: ")
            new_id = str(len(movies) + 1)
            m_data = {"id": new_id, "title": title, "genre": input("Genre: ")}
            m_logic.add_movie(movies, m_data)
            print(f"Success! Movie assigned ID: {new_id}")
            
        elif choice == "2":
            sid = input("Showtime ID: ")
            mid = input("Movie ID: ")
            s_data = {"id": sid, "movie_id": mid, "date": input("Date (YYYY-MM-DD): ")}
            m_logic.schedule_showtime(showtimes, s_data)
            seat_maps[sid] = s_logic.initialize_seat_map({"rows": 8, "seats_per_row": 12})
            print(f"Showtime scheduled for '{get_movie_title(movies, mid)}'.")
            
        elif choice == "3": break
        st_logic.save_state(BASE_DIR, movies, showtimes, bookings)

def customer_menu(movies, showtimes, seat_maps, bookings):
    while True:
        print("\n--- CUSTOMER MENU ---")
        print("1. List Showtimes\n2. Book Ticket\n3. Cancel Booking\n4. Back")
        choice = input("Selection: ")
        
        if choice == "1":
            print("\n--- AVAILABLE SHOWTIMES ---")
            for s in showtimes:
                title = get_movie_title(movies, s['movie_id'])
                print(f"ID: {s['id']} | Movie: {title} | Date: {s['date']}")
                
        elif choice == "2":
            sid = input("Enter Showtime ID: ")
            if sid in seat_maps:
                print(s_logic.render_seat_map(seat_maps[sid]))
                seat = input("Select Seat (e.g., A1): ").upper()
                
                if s_logic.is_seat_available(seat_maps[sid], seat):
                    price = 240 if seat[0] in ['A', 'B'] else 180
                    print(f"\nTotal Price (incl. VAT): {price} USD")
                    
                    if input("Confirm payment? (y/n): ").lower() == 'y':
                        s_logic.reserve_seat(seat_maps[sid], seat)
                        b_data = {
                            "showtime_id": sid,
                            "seats": [seat], 
                            "price": price, 
                            "email": input("Enter your email: ")
                        }
                        b_logic.create_booking(bookings, seat_maps, b_data)
                        print("Booking successful!")
                else: print("Error: Seat is already taken!")
            else: print("Error: Invalid Showtime ID!")

        elif choice == "3":
            email = input("Enter your email to find bookings: ")
            user_bookings = [b for b in bookings if b['email'] == email]
            
            if not user_bookings:
                print("No bookings found for this email.")
            else:
                for i, b in enumerate(user_bookings):
                    print(f"{i+1}. Showtime: {b['showtime_id']} | Seat: {b['seats'][0]}")
                
                try:
                    c_idx = int(input("Select booking to cancel (number): ")) - 1
                    target = user_bookings[c_idx]
                    
                    # Logic: 1. Remove from bookings list, 2. Free the seat in seat_map
                    bookings.remove(target)
                    s_logic.initialize_seat_map(seat_maps[target['showtime_id']]) # Refresh logic
                    for b_remain in bookings:
                        if b_remain['showtime_id'] == target['showtime_id']:
                            s_logic.reserve_seat(seat_maps[b_remain['showtime_id']], b_remain['seats'][0])
                    
                    print("Booking cancelled successfully!")
                except:
                    print("Invalid selection.")
            
        elif choice == "4": break
        st_logic.save_state(BASE_DIR, movies, showtimes, bookings)

def main():
    if not os.path.exists(BASE_DIR): os.makedirs(BASE_DIR)
    movies, showtimes, bookings = st_logic.load_state(BASE_DIR)
    seat_maps = {s['id']: s_logic.initialize_seat_map({"rows": 8, "seats_per_row": 12}) for s in showtimes}
    
    for b in bookings:
        sid = b.get('showtime_id')
        s_id = b.get('seats') or b.get('seat')
        if sid in seat_maps and s_id:
            target = s_id if not isinstance(s_id, list) else s_id[0]
            s_logic.reserve_seat(seat_maps[sid], target)

    while True:
        print("\n=== MOVIE BOOKING SYSTEM ===")
        print("1. Customer\n2. Admin\n3. Exit")
        role = input("Select Role: ")
        if role == "1": customer_menu(movies, showtimes, seat_maps, bookings)
        elif role == "2": admin_menu(movies, showtimes, seat_maps, bookings)
        elif role == "3": break
    st_logic.save_state(BASE_DIR, movies, showtimes, bookings)

if __name__ == "__main__":
    main()