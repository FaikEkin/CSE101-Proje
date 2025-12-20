import seating as s
import bookings as b


def run_automated_tests():
    print("--- Testler Başlatılıyor ---")

    # 1. Koltuk Haritası ve Seçim Testi [cite: 39, 82]
    test_map = s.initialize_seat_map({"rows": 2, "seats_per_row": 5})
    assert s.is_seat_available(test_map, "A1") == True

    # 2. Rezervasyon ve Çifte Rezervasyon Engelleme Testi [cite: 11, 77]
    s_maps = {"SHOW1": test_map}
    booking_data = {"showtime_id": "SHOW1", "seats": ["A1"], "email": "test@user.com", "total_price": 100}
    res = b.create_booking([], s_maps, booking_data)
    assert res != {}  # İlk rezervasyon başarılı olmalı
    assert s.is_seat_available(test_map, "A1") == False  # Koltuk dolmuş olmalı

    # Aynı koltuğu tekrar almayı dene
    res_fail = b.create_booking([], s_maps, booking_data)
    assert res_fail == {}  # İkinci deneme başarısız olmalı (Double Booking koruması)

    # 3. İptal ve Koltuk Tahliye Testi [cite: 45, 48]
    bookings_list = [res]
    b.cancel_booking(bookings_list, res['booking_id'], s_maps)
    assert s.is_seat_available(test_map, "A1") == True  # İptal sonrası koltuk boşalmalı

    print("Tebrikler! Tüm testler (Koltuk Seçimi, Çifte Rezervasyon Engelleme ve İptal) başarıyla geçti. [cite: 101]")


if __name__ == "__main__":
    run_automated_tests()