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
    return "Bilinmeyen Film"

def admin_menu(movies, showtimes, seat_maps, bookings):
    while True:
        print("\n--- YÖNETİCİ PANELİ ---")
        print("1. Film Ekle\n2. Seans Planla\n3. Geri")
        choice = input("Seçim: ")
        if choice == "1":
            t = input("Film Adı: ")
            new_id = str(len(movies) + 1)
            m_data = {"id": new_id, "title": t, "genre": input("Tür: ")}
            m_logic.add_movie(movies, m_data)
            print(f"Eklendi! ID: {new_id}")
        elif choice == "2":
            sid = input("Seans ID: ")
            mid = input("Film ID: ")
            s_data = {"id": sid, "movie_id": mid, "date": input("Tarih: ")}
            m_logic.schedule_showtime(showtimes, s_data)
            seat_maps[sid] = s_logic.initialize_seat_map({"rows": 8, "seats_per_row": 12})
            print("Seans ve koltuk haritası hazır!")
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
                    
                    base = 200 if seat[0] in ['A', 'B'] else 150
                    tax = base * 0.20
                    total = base + tax
                    print(f"\nBilet: {base} TL | KDV: {tax} TL | Toplam: {total} TL")
                    
                    if input("Onaylıyor musunuz? (y/n): ").lower() == 'y':
                        
                        s_logic.reserve_seat(seat_maps[sid], seat)
                        
                        
                        b_data = {"showtime_id": sid, "seat": seat, "price": total, "email": input("E-posta: ")}
                        bookings.append(b_data)
                        
                        
                        st_logic.save_state(BASE_DIR, movies, showtimes, bookings)
                        print("İşlem Başarılı! Koltuk kapatıldı.")
                else:
                    print("HATA: Bu koltuk zaten dolu!")
            else: print("Geçersiz Seans!")
        elif choice == "3": break

def main():
    if not os.path.exists(BASE_DIR): os.makedirs(BASE_DIR)
    movies, showtimes, bookings = st_logic.load_state(BASE_DIR)
    
    seat_maps = {s['id']: s_logic.initialize_seat_map({}) for s in showtimes}
    
    
    for b in bookings:
        if b['showtime_id'] in seat_maps:
            s_logic.reserve_seat(seat_maps[b['showtime_id']], b['seat'])

    while True:
        print("\n=== SİNEMA SİSTEMİ ===")
        print("1. Müşteri\n2. Admin\n3. Çıkış")
        r = input("Rol: ")
        if r == "1": customer_menu(movies, showtimes, seat_maps, bookings)
        elif r == "2": admin_menu(movies, showtimes, seat_maps, bookings)
        elif r == "3": break

if __name__ == "__main__":
    main()