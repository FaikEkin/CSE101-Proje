import json

def load_movies(path: str) -> list:
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_movies(path: str, movies: list) -> None:
    with open(path, 'w') as f:
        json.dump(movies, f, indent=4)

def add_movie(movies: list, movie_data: dict) -> dict:
    movies.append(movie_data)
    return movie_data

def schedule_showtime(showtimes: list, showtime_data: dict) -> dict:
    showtimes.append(showtime_data)
    return showtime_data

def list_showtimes(showtimes: list, movie_id: str | None = None, date: str | None = None) -> list:
    filtered = showtimes
    if movie_id:
        filtered = [s for s in filtered if s.get('movie_id') == movie_id]
    if date:
        filtered = [s for s in filtered if s.get('date') == date]
    return filtered

def update_showtime(showtimes: list, showtime_id: str, updates: dict) -> dict:
    for showtime in showtimes:
        if showtime.get('id') == showtime_id:
            showtime.update(updates)
            return showtime
    return {}