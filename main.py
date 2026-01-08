import os
import movies as m_logic
import seating as s_logic
import bookings as b_logic
import storage as st_logic

BASE_DIR = "data"


def get_movie_title(movies, movie_id):
    for movie in movies:
        if movie['id'] == movie_id:
            return movie['title']
    return "Unknown Movie"

def admin_menu(movies, showtimes, seat_maps, bookings):
    while True:
        print("\n--- ADMIN PANEL ---")
        print("1. Add Movie (Kataloğa Ekle)\n2. Schedule Showtime (Seans Planla)\n3. Back")
        choice = input("Seçiminiz: ")
        
        if choice == "1":
            title = input("Film Adı: ")
            new_id = str(len(movies) + 1) # Otomatik ID
            m_data = {"id": new_id, "title": title, "genre": input("Tür: ")}
            m_logic.add_movie(movies, m_data)
            print(f"Film eklendi! Atanan Film ID: {new_id}")
            
        elif choice == "2":
            
            sid = input("Seans ID (Örn: 101): ")
            mid = input("Hangi Film? (Film ID'sini yazın): ")
            s_data = {"id": sid, "movie_id": mid, "date": input("Tarih (YYYY-MM-DD): ")}
            m_logic.schedule_showtime(showtimes, s_data)
            seat_maps[sid] = s_logic.initialize_seat_map({"rows": 8, "seats_per_row": 12})
            print(f"Seans planlandı! '{get_movie_title(movies, mid)}' filmi için seans hazır.")
            
        elif choice == "3": break
        st_logic.save_state(BASE_DIR, movies, showtimes, bookings)

def customer_menu(movies, showtimes, seat_maps, bookings):
    while True:
        print("\n--- CUSTOMER MENU ---")
        print("1. List Showtimes\n2. Book Ticket\n3. Back")
        choice = input("Seçiminiz: ")
        
        if choice == "1":
            print("\n--- MEVCUT SEANSLAR ---")
            for s in showtimes:
                
                title = get_movie_title(movies, s['movie_id'])
                print(f"Seans No: {s['id']} | Film: {title} | Tarih: {s['date']}")
                
        elif choice == "2":
            sid = input("Seans No girin: ")
            if sid in seat_maps:
                print(s_logic.render_seat_map(seat_maps[sid]))
                seat = input("Koltuk Seçin (Örn: A1): ")
                
                print("Bilet başarıyla alındı!")
            else: print("Geçersiz seans!")
            
        elif choice == "3": break
        st_logic.save_state(BASE_DIR, movies, showtimes, bookings)

def main():
    movies, showtimes, bookings = st_logic.load_state(BASE_DIR)
    seat_maps = {s['id']: s_logic.initialize_seat_map({}) for s in showtimes}
    
    while True:
        print("\n=== MOVIE BOOKING SYSTEM ===")
        print("1. Customer\n2. Admin\n3. Exit")
        role = input("Rol seçin: ")
        if role == "1": customer_menu(movies, showtimes, seat_maps, bookings)
        elif role == "2": admin_menu(movies, showtimes, seat_maps, bookings)
        elif role == "3": break
    st_logic.save_state(BASE_DIR, movies, showtimes, bookings)

if __name__ == "__main__":
    main()