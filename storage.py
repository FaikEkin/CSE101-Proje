import json
import shutil
import os
from datetime import datetime

def load_state(base_dir: str) -> tuple[list, dict, list]:
    try:
        with open(os.path.join(base_dir, 'movies.json'), 'r') as f:
            movies = json.load(f)
        with open(os.path.join(base_dir, 'showtimes.json'), 'r') as f:
            showtimes = json.load(f)
        with open(os.path.join(base_dir, 'bookings.json'), 'r') as f:
            bookings = json.load(f)
        return movies, showtimes, bookings
    except (FileNotFoundError, json.JSONDecodeError):
        return [], [], []

def save_state(base_dir: str, movies: list, showtimes: list, bookings: list) -> None:
    os.makedirs(base_dir, exist_ok=True)
    with open(os.path.join(base_dir, 'movies.json'), 'w') as f:
        json.dump(movies, f, indent=4)
    with open(os.path.join(base_dir, 'showtimes.json'), 'w') as f:
        json.dump(showtimes, f, indent=4)
    with open(os.path.join(base_dir, 'bookings.json'), 'w') as f:
        json.dump(bookings, f, indent=4)

def backup_state(base_dir: str, backup_dir: str) -> list[str]:
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backups = []
    for filename in ['movies.json', 'showtimes.json', 'bookings.json']:
        src = os.path.join(base_dir, filename)
        if os.path.exists(src):
            dst = os.path.join(backup_dir, f"{timestamp}_{filename}")
            shutil.copy2(src, dst)
            backups.append(dst)
    return backups

def validate_showtime(showtime: dict) -> bool:
    required = ['id', 'movie_id', 'date', 'time', 'screen']
    return all(k in showtime for k in required)