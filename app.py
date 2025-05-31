from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Dummy data for movies
movies_db = [
    {"id": 1, "title": "Inception", "director": "Christopher Nolan"},
    {"id": 2, "title": "The Matrix", "director": "The Wachowskis"}
]

# In-memory review storage
reviews_db = []

# Route: Get all movies
@app.route('/movies', methods=['GET'])
def get_movies():
    return jsonify(movies_db)

# Route: Add a new movie
@app.route('/movies', methods=['POST'])
def add_movie():
    data = request.get_json()
    required_keys = {"id", "title", "director"}

    if not data or not required_keys.issubset(data):
        return jsonify({"error": "Invalid movie data"}), 400
    movies_db.append(data)
    return jsonify(data), 201

# Route: Get a specific movie by ID
@app.route('/movie/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = next((m for m in movies_db if m["id"] == movie_id), None)
    return jsonify(movie) if movie else ('Not Found', 404)

# Route: User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    VALID_USERNAME = "admin"
    VALID_PASSWORD = "secret"

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            return f"Logged in as {username}", 200
        else:
            return "Invalid credentials", 401
    return render_template("login.html")

# Home page displaying movies
@app.route('/')
def home():
    return render_template("home.html", movies=movies_db)

# HTML reviews page
@app.route('/reviews')
def review_list():
    return render_template("reviews.html", reviews=reviews_db)

# HTML rating form
@app.route('/rate_movies', methods=['GET'])
def rate_movies():
    return render_template("rate_movies.html", movies=movies_db)

# ✅ JSON API: Get all reviews
@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    return jsonify(reviews_db)

# ✅ JSON API: Post a new review
@app.route('/api/reviews', methods=['POST'])
def post_review():
    review_data = request.get_json()

    # Only allow reviews for movie ID 1
    if review_data.get('movie_id') != 1:
        return jsonify({"error": "Reviews only allowed for movie with id=1"}), 400

    reviews_db.append(review_data)
    return jsonify(review_data), 201

# Web form submission (form-urlencoded)
@app.route('/submit_rating', methods=['POST'])
def submit_rating():
    try:
        movie_id = int(request.form.get("movie_id"))
        rating = int(request.form.get("rating"))
        review = request.form.get("review")

        if not (1 <= rating <= 5):
            return "Invalid rating. Must be 1-5", 400

        review_entry = {
            "movie_id": movie_id,
            "rating": rating,
            "review": review
        }

        reviews_db.append(review_entry)
        return f"Rating submitted for movie ID {movie_id}", 201

    except Exception as e:
        return f"Error: {e}", 400

if __name__ == '__main__':
    app.run(debug=True)
