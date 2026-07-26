from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle

app = Flask(__name__)
CORS(app)

# Load Model
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))


def recommend(movie):

    movie = movie.lower()

    movie_list = movies[movies["title"].str.lower() == movie]

    if movie_list.empty:
        return ["Movie Not Found"]

    index = movie_list.index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
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

    movie = data.get("movie")

    result = recommend(movie)

    return jsonify({
        "recommendations": result
    })


if __name__ == "__main__":
    app.run(debug=True)