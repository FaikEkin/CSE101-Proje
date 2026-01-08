import os
import movies as m_logic
import seating as s_logic
import bookings as b_logic
import storage as st_logic
import reports as r_logic

BASE_DIR = "data"

def get_movie_title(movies, movie_id):
    for movie in movies:
        if str(movie['id']) == str(movie_id):
            return movie['title']
    return "Unknown Movie"

def admin_menu(movies, showtimes, seat_maps, bookings):
    while True:
        print("\n--- ADMIN PANEL ---")
        
        print("1. Add Movie\n2. Schedule Showtime\n3. View Reports\n4. Back")
        choice = input("Selection: ")
        
        if choice == "1":
            title = input("Movie Title: ")
            new_id = str(len(movies) + 1)
            m_data = {"id": new_id, "title": title, "genre": input("Genre: ")}
            m_logic.add_movie(movies, m_data)
            print(f"Success! ID: {new_id}")
            
        elif choice == "2":
            sid = input("Showtime ID: ")
            mid = input("Movie ID: ")
            s_data = {"id": sid, "movie_id": mid, "date": input("Date: ")}
            m_logic.schedule_showtime(showtimes, s_data)
            seat_maps[sid] = s_logic.initialize_seat_map({"rows": 8, "seats_per_row": 12})
            print("Showtime scheduled.")

	elif choice == "3":
            print("\n" + "="*45)
            print(f"{'MOVIE TITLE':<20} | {'ID':<5} | {'OCCUPANCY':<10}")
            print("-" * 45)
            
            # Toplam kapasite (8x12 matrisimize göre)
            TOTAL_CAPACITY = 96 
            total_revenue = 0
            
            for s in showtimes:
                # Bu seansa ait biletleri say
                sold_count = len([b for b in bookings if str(b['showtime_id']) == str(s['id'])])
                occ_rate = (sold_count / TOTAL_CAPACITY) * 100
                title = get_movie_title(movies, s['movie_id'])
                
                # Seans başı gelir hesabı
                s_revenue = sum(b['price'] for b in bookings if str(b['showtime_id']) == str(s['id']))
                total_revenue += s_revenue
                
                print(f"{title[:20]:<20} | {s['id']:<5} | {occ_rate:>8.1f}%")
            
            print("-" * 45)
            print(f"TOTAL REVENUE: {total_revenue:.2f} USD")
            print(f"TOTAL TICKETS: {len(bookings)}")
            print("="*45)
            
        elif choice == "4": break
        st_logic.save_state(BASE_DIR, movies, showtimes, bookings)

def customer_menu(movies, showtimes, seat_maps, bookings):
    while True:
        print("\n--- CUSTOMER MENU ---")
        print("1. List Showtimes\n2. Book Ticket\n3. Cancel Booking\n4. Back")
        choice = input("Selection: ").strip() # Boşlukları temizle
        
        if choice == "1":
            print("\n--- AVAILABLE SHOWTIMES ---")
            for s in showtimes:
                title = get_movie_title(movies, s['movie_id'])
                print(f"ID: {s['id']} | Movie: {title} | Date: {s['date']}")
                
        elif choice == "2":
            sid = input("Enter Showtime ID: ").strip()
            if sid in seat_maps:
                print(s_logic.render_seat_map(seat_maps[sid]))
                seat = input("Select Seat (e.g., A1): ").strip().upper()
                
                if s_logic.is_seat_available(seat_maps[sid], seat):
                    price = 240 if seat[0] in ['A', 'B'] else 180
                    print(f"\nTotal Price (incl. VAT): {price} USD")
                    
                    if input("Confirm payment? (y/n): ").strip().lower() == 'y':
                        # Bilet verisini hazırlıyoruz
                        b_data = {
                            "showtime_id": sid,
                            "seats": [seat], 
                            "price": price, 
                            "email": input("Enter your email: ").strip().lower() # Küçük harf ve temiz
                        }
                        
                        # Modülleri çağırıyoruz
                        s_logic.reserve_seat(seat_maps[sid], seat)
                        b_logic.create_booking(bookings, seat_maps, b_data)
                        
                        # EĞER bookings.py listeye eklemiyorsa burada manuel garantiye alıyoruz:
                        if b_data not in bookings:
                            bookings.append(b_data)
                            
                        print("Booking successful!")
                else: print("Error: Seat is already taken!")
            else: print("Error: Invalid Showtime ID!")

        elif choice == "3":
            email = input("Enter your email to find bookings: ").strip().lower()
            # E-posta eşleşmesi için listeyi tarıyoruz
            user_bookings = [b for b in bookings if str(b.get('email', '')).lower() == email]
            
            if not user_bookings:
                print(f"No bookings found for email: {email}")
            else:
                print("\n--- YOUR BOOKINGS ---")
                for i, b in enumerate(user_bookings):
                    s_id = b.get('seats', ['?'])[0]
                    print(f"{i+1}. Showtime: {b['showtime_id']} | Seat: {s_id}")
                
                try:
                    c_input = input("Select booking to cancel (number) or 'n' to exit: ").strip()
                    if c_input.lower() != 'n':
                        c_idx = int(c_input) - 1
                        target = user_bookings[c_idx]
                        
                        # Listeden sil
                        bookings.remove(target)
                        
                        # Haritayı sıfırla ve kalan biletleri tekrar işaretle (Refresh)
                        seat_maps[target['showtime_id']] = s_logic.initialize_seat_map({"rows": 8, "seats_per_row": 12})
                        for b_rem in bookings:
                            if b_rem['showtime_id'] == target['showtime_id']:
                                s_id_rem = b_rem.get('seats', [None])[0]
                                if s_id_rem: s_logic.reserve_seat(seat_maps[b_rem['showtime_id']], s_id_rem)
                        
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