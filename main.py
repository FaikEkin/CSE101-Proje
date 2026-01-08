import os
import movies as m_logic      # Film ve seans işlemleri
import seating as s_logic     # Matris ve koltuk işlemleri
import bookings as b_logic    # Rezervasyon ve fiyatlandırma
import storage as st_logic     # JSON yükleme/kaydetme

BASE_DIR = "data"

def get_movie_title(movies, movie_id):
    """Filmi kataloğunda bulup ismini döndürür."""
    for movie in movies:
        if str(movie['id']) == str(movie_id):
            return movie['title']
    return "Bilinmeyen Film"

def admin_menu(movies, showtimes, seat_maps, bookings):
    while True:
        print("\n--- YÖNETİCİ PANELİ ---")
        print("1. Film Ekle\n2. Seans Planla\n3. Geri")
        choice = input("Seçim: ")
        
        if choice == "1":
            # add_movie fonksiyonunu movies.py'dan çağırıyoruz
            m_data = {"id": str(len(movies)+1), "title": input("Film Adı: "), "genre": input("Tür: ")}
            m_logic.add_movie(movies, m_data)
            print(f"Film kataloğa eklendi. ID: {m_data['id']}")
            
        elif choice == "2":
            
            sid = input("Seans ID: ")
            mid = input("Film ID: ")
            s_data = {"id": sid, "movie_id": mid, "date": input("Tarih: ")}
            m_logic.schedule_showtime(showtimes, s_data)
            seat_maps[sid] = s_logic.initialize_seat_map({"rows": 8, "seats_per_row": 12})
            print("Seans planlandı ve boş salon oluşturuldu.")
            
        elif choice == "3": break
        st_logic.save_state(BASE_DIR, movies, showtimes, bookings)

def customer_menu(movies, showtimes, seat_maps, bookings):
    while True:
        print("\n--- MÜŞTERİ MENÜSÜ ---")
        print("1. Seansları Listele\n2. Bilet Al\n3. Geri")
        choice = input("Seçim: ")
        
        if choice == "1":
            for s in showtimes:
                print(f"ID: {s['id']} | Film: {get_movie_title(movies, s['movie_id'])} | Tarih: {s['date']}")
        
        elif choice == "2":
            sid = input("Seans No: ")
            if sid in seat_maps:
                
                print(s_logic.render_seat_map(seat_maps[sid]))
                seat = input("Koltuk (Örn: A1): ").upper()
                
                
                if s_logic.is_seat_available(seat_maps[sid], seat):
                    
                    price = 240 if seat[0] in ['A', 'B'] else 180 # %20 KDV dahil hali
                    print(f"Toplam Ücret (KDV Dahil): {price} TL")
                    
                    if input("Onaylıyor musunuz? (y/n): ").lower() == 'y':
                        
                        s_logic.reserve_seat(seat_maps[sid], seat)
                        
                        
                        b_data = {"showtime_id": sid, "seat": seat, "price": price, "email": input("E-posta: ")}
                        b_logic.create_booking(bookings, seat_maps, b_data)
                        print("Biletiniz başarıyla oluşturuldu!")
                else: print("HATA: Koltuk dolu!")
            else: print("Geçersiz seans!")
        elif choice == "3": break
        st_logic.save_state(BASE_DIR, movies, showtimes, bookings)

def main():
    if not os.path.exists(BASE_DIR): os.makedirs(BASE_DIR)
    
    movies, showtimes, bookings = st_logic.load_state(BASE_DIR)
    
    
    seat_maps = {s['id']: s_logic.initialize_seat_map({"rows": 8, "seats_per_row": 12}) for s in showtimes}
    
    
    for b in bookings:
        sid = b.get('showtime_id')
        seat_id = b.get('seat') or b.get('seats') 
        if sid in seat_maps and seat_id:
            s_logic.reserve_seat(seat_maps[sid], seat_id if not isinstance(seat_id, list) else seat_id[0])

    while True:
        print("\n=== SİNEMA REZERVASYON SİSTEMİ ===")
        print("1. Müşteri Girişi\n2. Admin Girişi\n3. Çıkış")
        r = input("Rol: ")
        if r == "1": customer_menu(movies, showtimes, seat_maps, bookings)
        elif r == "2": admin_menu(movies, showtimes, seat_maps, bookings)
        elif r == "3": break
    st_logic.save_state(BASE_DIR, movies, showtimes, bookings)

if __name__ == "__main__":
    main()