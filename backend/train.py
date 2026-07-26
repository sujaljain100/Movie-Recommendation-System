import pandas as pd
import ast
import pickle
from sklearn.feature_extraction.text import CountVectorizer

# ==========================
# Load Datasets
# ==========================

movies = pd.read_csv("data/tmdb_5000_movies.csv")
credits = pd.read_csv("data/tmdb_5000_credits.csv")

movies = movies.merge(credits, on="title")

movies = movies[
    [
        "movie_id",
        "title",
        "overview",
        "genres",
        "keywords",
        "cast",
        "crew",
    ]
]

movies.dropna(inplace=True)


# ==========================
# Helper Functions
# ==========================

def convert(text):
    result = []
    for item in ast.literal_eval(text):
        result.append(item["name"])
    return result


def convert_cast(text):
    result = []
    for item in ast.literal_eval(text)[:3]:
        result.append(item["name"])
    return result


def fetch_director(text):
    for item in ast.literal_eval(text):
        if item["job"] == "Director":
            return [item["name"]]
    return []


# ==========================
# Feature Engineering
# ==========================

movies["genres"] = movies["genres"].apply(convert)
movies["keywords"] = movies["keywords"].apply(convert)
movies["cast"] = movies["cast"].apply(convert_cast)
movies["crew"] = movies["crew"].apply(fetch_director)

movies["overview"] = movies["overview"].apply(lambda x: x.split())

movies["genres"] = movies["genres"].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies["keywords"] = movies["keywords"].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies["cast"] = movies["cast"].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies["crew"] = movies["crew"].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies["tags"] = (
    movies["overview"]
    + movies["genres"]
    + movies["keywords"]
    + movies["cast"]
    + movies["crew"]
)

new_df = movies[["movie_id", "title", "tags"]]

new_df["tags"] = new_df["tags"].apply(lambda x: " ".join(x))
new_df["tags"] = new_df["tags"].apply(lambda x: x.lower())

# ==========================
# Vectorizer
# ==========================

cv = CountVectorizer(
    max_features=5000,
    stop_words="english"
)

cv.fit(new_df["tags"])

# ==========================
# Save Files
# ==========================

pickle.dump(new_df, open("movies.pkl", "wb"))

pickle.dump(cv, open("vectorizer.pkl", "wb"))

print("Training Completed Successfully")