from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

# Load Data
movies = pickle.load(open("movies.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Create vectors once when app starts
vectors = vectorizer.transform(movies["tags"])


def recommend(movie):

    movie = movie.lower()

    movie_list = movies[movies["title"].str.lower() == movie]

    if movie_list.empty:
        return ["Movie Not Found"]

    index = movie_list.index[0]

    similarity = cosine_similarity(
        vectors[index],
        vectors
    ).flatten()

    distances = sorted(
        list(enumerate(similarity)),
        key=lambda x: x[1],
        reverse=True
    )

    recommended = []

    for i in distances[1:7]:
        recommended.append(
            movies.iloc[i[0]].title
        )

    return recommended


@app.route("/")
def home():
    return jsonify({
        "message": "Movie Recommendation API Running"
    })


@app.route("/recommend", methods=["POST"])
def recommendation():

    data = request.get_json()

    movie = data.get("movie", "")

    result = recommend(movie)

    return jsonify({
        "recommendations": result
    })


if __name__ == "__main__":
    app.run(debug=True)