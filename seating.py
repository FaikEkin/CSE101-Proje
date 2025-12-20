def initialize_seat_map(screen_config: dict) -> dict:
    rows = screen_config.get('rows', 8)
    seats_per_row = screen_config.get('seats_per_row', 12)
    seat_map = {}

    for row_idx in range(rows):
        row_letter = chr(65 + row_idx)
        for num in range(1, seats_per_row + 1):
            seat_code = f"{row_letter}{num}"
            tier = "premium" if row_idx < 2 else "standard"
            seat_map[seat_code] = {
                "status": "available",
                "tier": tier
            }
    return seat_map


def render_seat_map(seat_map: dict) -> str:
    output = "\n   " + " ".join(f"{i:2}" for i in range(1, 13)) + "\n"
    current_row = ""

    for seat_code, data in seat_map.items():
        row = seat_code[0]
        if row != current_row:
            if current_row != "": output += "\n"
            output += f"{row}  "
            current_row = row

        symbol = "○" if data["status"] == "available" else "●"
        output += f"{symbol}  "

    legend = "\n\nLegend: ○ Available, ● Reserved/Sold"
    return output + legend


def is_seat_available(seat_map: dict, seat_code: str) -> bool:
    seat = seat_map.get(seat_code)
    return seat is not None and seat["status"] == "available"


def reserve_seat(seat_map: dict, seat_code: str) -> dict:
    if is_seat_available(seat_map, seat_code):
        seat_map[seat_code]["status"] = "reserved"
    return seat_map


def release_seat(seat_map: dict, seat_code: str) -> dict:
    if seat_code in seat_map:
        seat_map[seat_code]["status"] = "available"
    return seat_map